import re
from typing import List, Dict, Any
import tiktoken

class TextChunker:
    """
    Utility class for chunking text into smaller pieces for embedding and retrieval.
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 50, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Target size of each chunk in tokens
            overlap: Number of overlapping tokens between chunks
            model_name: Name of the model to use for tokenization
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Chunk the given text into smaller pieces.

        Args:
            text: The text to chunk
            metadata: Metadata to include with each chunk

        Returns:
            List of dictionaries containing chunk content and metadata
        """
        if not text:
            return []

        # Split text into sentences to avoid breaking in the middle of sentences
        sentences = self._split_into_sentences(text)

        # Convert sentences to tokens
        sentence_tokens = [self.tokenizer.encode(sentence) for sentence in sentences]

        chunks = []
        current_chunk_tokens = []
        current_chunk_start_idx = 0

        for sentence_idx, sentence_token in enumerate(sentence_tokens):
            # If adding this sentence would exceed the chunk size
            if len(current_chunk_tokens) + len(sentence_token) > self.chunk_size:
                # Finalize the current chunk if it has content
                if current_chunk_tokens:
                    chunk_text = self.tokenizer.decode(current_chunk_tokens)
                    chunk_metadata = self._create_chunk_metadata(
                        metadata or {},
                        current_chunk_start_idx,
                        sentence_idx - 1,
                        len(sentences)
                    )

                    chunks.append({
                        'content': chunk_text.strip(),
                        'metadata': chunk_metadata
                    })

                # Start a new chunk with overlap
                if len(sentence_token) > self.chunk_size:
                    # If the sentence is longer than the chunk size, split it
                    subchunks = self._split_long_sentence(sentence_token)
                    for subchunk in subchunks:
                        chunks.append({
                            'content': self.tokenizer.decode(subchunk).strip(),
                            'metadata': self._create_chunk_metadata(
                                metadata or {},
                                sentence_idx,
                                sentence_idx,
                                len(sentences)
                            )
                        })
                    current_chunk_tokens = []
                    current_chunk_start_idx = sentence_idx + 1
                else:
                    # Start new chunk with overlap from the previous chunk
                    if self.overlap > 0 and len(current_chunk_tokens) >= self.overlap:
                        # Take the last 'overlap' tokens from the previous chunk
                        current_chunk_tokens = current_chunk_tokens[-self.overlap:]
                        current_chunk_start_idx = sentence_idx
                    else:
                        current_chunk_tokens = []
                        current_chunk_start_idx = sentence_idx

                    current_chunk_tokens.extend(sentence_token)
            else:
                current_chunk_tokens.extend(sentence_token)

        # Add the final chunk if there are remaining tokens
        if current_chunk_tokens:
            chunk_text = self.tokenizer.decode(current_chunk_tokens)
            chunk_metadata = self._create_chunk_metadata(
                metadata or {},
                current_chunk_start_idx,
                len(sentence_tokens) - 1,
                len(sentences)
            )

            chunks.append({
                'content': chunk_text.strip(),
                'metadata': chunk_metadata
            })

        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex.

        Args:
            text: The text to split

        Returns:
            List of sentences
        """
        # This regex handles various sentence endings and abbreviations
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        sentences = re.split(sentence_pattern, text)

        # Clean up sentences
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

        return sentences

    def _split_long_sentence(self, tokens: List[int]) -> List[List[int]]:
        """
        Split a long sentence into smaller chunks.

        Args:
            tokens: The tokens to split

        Returns:
            List of token lists
        """
        subchunks = []
        for i in range(0, len(tokens), self.chunk_size):
            subchunk = tokens[i:i + self.chunk_size]
            subchunks.append(subchunk)
        return subchunks

    def _create_chunk_metadata(self, base_metadata: Dict[str, Any], start_idx: int, end_idx: int, total_sentences: int) -> Dict[str, Any]:
        """
        Create metadata for a chunk with position information.

        Args:
            base_metadata: Base metadata to extend
            start_idx: Starting sentence index
            end_idx: Ending sentence index
            total_sentences: Total number of sentences

        Returns:
            Extended metadata dictionary
        """
        chunk_metadata = base_metadata.copy()
        chunk_metadata['sentence_start_idx'] = start_idx
        chunk_metadata['sentence_end_idx'] = end_idx
        chunk_metadata['total_sentences'] = total_sentences
        chunk_metadata['chunk_position'] = f"{start_idx+1}-{end_idx+1}/{total_sentences}"
        return chunk_metadata


def chunk_textbook_content(content: str, chunk_size: int = 512, overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Convenience function to chunk textbook content.

    Args:
        content: The textbook content to chunk
        chunk_size: Target size of each chunk in tokens
        overlap: Number of overlapping tokens between chunks

    Returns:
        List of dictionaries containing chunk content and metadata
    """
    chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
    return chunker.chunk_text(content)