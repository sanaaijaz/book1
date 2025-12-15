---
id: 0001
title: AI-native textbook project specification
stage: spec
date: 2025-12-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-textbook
branch: master
user: User
command: write AI-native textbook project specification
labels: ["specification", "ai-textbook", "rag", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - null
tests:
  - null
---

## Prompt

YouYou are an AI Specification Architect using Spec-Kit Plus.

Your task is to write a complete, structured, production-grade specification for a unified AI-native textbook project based on the following requirements:

---------------------------------------------------------------------
HACKATHON REQUIREMENTS (FULL SCOPE)
---------------------------------------------------------------------

1. The project is to create an AI-native textbook on *Physical AI & Humanoid Robotics*, using:
   - Docusaurus
   - Claude Code
   - Spec-Kit Plus

2. The textbook must be published on GitHub Pages or Vercel.

3. The project must include an integrated *Retrieval-Augmented Generation (RAG) chatbot* that uses:
   - OpenAI Agents / ChatKit SDK
   - FastAPI backend
   - Neon Serverless Postgres
   - Qdrant Cloud Free Tier
   - Ability to answer questions about the book
   - Ability to answer questions based on only user-selected text

4. Scoring:
   - 100 points for base functionality
   - +50 points for reusable intelligence using Claude Code Subagents & Agent Skills
   - +50 points for signup/signin using BetterAuth, with user background questions
   - +50 points for chapter personalization button
   - +50 points for Urdu translation button
   - Total possible: 250 points

5. Deliverables:
   - Public GitHub repo
   - Published book URL
   - Embedded RAG chatbot
   - 90-second demo video
   - WhatsApp for invitation

6. Timeline:
   - Submission: Nov 30, 2025 @ 06:00 PM
   - Live presentations same day

---------------------------------------------------------------------
COURSE OUTLINE (TEXTBOOK MUST COVER)
---------------------------------------------------------------------

Course: *Physical AI & Humanoid Robotics*

Module 1: ROS 2 — The Robotic Nervous System
- Nodes, Topics, Services
- rclpy agent-to-controller bridging
- URDF for humanoids

Module 2: Digital Twins — Gazebo & Unity
- Physics simulation
- Gravity, collisions
- LiDAR, IMU, Depth Camera simulation
- Unity rendering

Module 3: NVIDIA Isaac — The AI Robot Brain
- Isaac Sim
- Isaac ROS
- VSLAM, perception, navigation
- Nav2 for bipedal walking

Module 4: Vision-Language-Action (VLA)
- Whisper voice-to-action
- LLM cognitive planning
- High-level instruction → ROS 2 action sequence
- Capstone: Full autonomous humanoid

Weekly Breakdown:
Weeks 1–13 include Physical AI intro → ROS → Gazebo → Isaac → Humanoid robotics → Conversational robotics.

Assessments:
- ROS project
- Gazebo simulation
- Isaac perception pipeline
- Final humanoid capstone

---------------------------------------------------------------------
HARDWARE REQUIREMENTS (TEXTBOOK MUST DOCUMENT)
---------------------------------------------------------------------

1. Digital Twin Workstation (RTX 4070 Ti+ minimum, 64GB RAM, Ubuntu 22.04)
2. Jetson Orin Nano/NX Edge Kit
3. RealSense D435i camera
4. IMU
5. ReSpeaker mic
6. Robot options:
   - Unitree Go2
   - G1 / Robotis OP3 / Hiwonder (budget)
7. Lab architecture diagrams (Sim Rig → Jetson → Sensors → Robot)
8. Cloud-native “Ether Lab” option (AWS g5/g6e GPU instances)

---------------------------------------------------------------------
SPEC-KIT PLUS REQUIREMENTS
---------------------------------------------------------------------

Produce ONE unified specification that includes:

### 1. Project Overview
Define goals, scope, challenges, constraints, and intended audience.

### 2. Functional Requirements
- Book creation workflow
- RAG chatbot architecture
- Personalization system
- Urdu translation system
- Authentication workflow (BetterAuth)
- Claude Code Subagents & Skills

### 3. Non-Functional Requirements
- Performance
- Latency
- Accessibility
- UX consistency
- AI transparency
- Error handling

### 4. System Architecture
- Docusaurus → RAG → FastAPI → Neon → Qdrant
- Diagrams (in Mermaid or Spec-Kit architecture blocks)

### 5. Data Requirements
- User profiles
- Background questions
- Embeddings
- Chapter mapping
- Personalization metadata

### 6. API Specifications
- RAG endpoints
- Auth endpoints
- Personalization endpoints
- Translation endpoints

### 7. Book Structure
Create a full outline of every chapter based on the course modules, including:
- Learning objectives
- Example code
- Exercises
- Diagrams

### 8. Agent Architecture (Claude Code)
Define:
- Subagents
- Agent Skills
- Workflow automation
- Reusable intelligence

### 9. UI/UX Requirements
Buttons:
- “Ask AI”
- “Ask About Selected Text”
- “Personalize Chapter”
- “Translate to Urdu”

### 10. Success Criteria
Mapping to:
- 100 core points
- +150 bonus points

### 11. Deliverables
Exact project output and folder structure.

### 12. Implementation Roadmap
Phased plan from setup → writing → RAG → auth → personalization.

---------------------------------------------------------------------
OUTPUT FORMAT REQUIREMENTS
---------------------------------------------------------------------

When writing the specification:

- Use Spec-Kit Plus formatting conventions
- Be extremely structured and hierarchical
- Use headings, numbered sections, architecture blocks, tables, and diagrams
- Avoid narrative prose—write like an engineering specification
- Include code snippets where appropriate (JSON, API schema, YAML, Python)
- Produce a complete, production-ready specification

---------------------------------------------------------------------

NOW WRITE THE COMPLETE SPECIFICATION.

## Response snapshot

I will now write a complete, structured, production-grade specification for a unified AI-native textbook project based on the provided requirements. I will ensure the specification adheres to Spec-Kit Plus formatting conventions, including headings, numbered sections, architecture blocks, tables, and diagrams, while avoiding narrative prose. I will also include code snippets where appropriate. I will use the `TodoWrite` tool to break down the task of writing the specification into manageable steps, covering each required section. First, I will create a PHR for this user prompt.

## Outcome

- ✅ Impact: N/A
- 🧪 Tests: N/A
- 📁 Files: N/A
- 🔁 Next prompts: N/A
- 🧠 Reflection: N/A

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
