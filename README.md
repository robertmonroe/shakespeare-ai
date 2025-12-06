# Libriscribe 2.0 - AI-Powered Book Creation & Automated Developmental Editing

**Transform your ideas into polished manuscripts with AI-powered writing and professional-grade automated editing.**

---

## 🎯 What is Libriscribe?

Libriscribe is an intelligent book creation system that doesn't just generate text—it **thinks like a professional editor**. From initial concept to publication-ready manuscript, Libriscribe handles the entire creative and editorial workflow.

### Key Features

✨ **Natural Language Creative Control** - Tell the AI what you want in plain English  
📊 **Automated Report Analysis** - Import reports from AutoCrit, ProWritingAid, Marlowe, etc.  
🎬 **Director Agent** - Make creative changes across your entire project instantly  
🔄 **Complete Consistency** - All files (characters, outline, scenes, chapters) stay synchronized  
👁️ **Vision Analysis** - Analyzes charts and graphs from editorial reports  
📝 **Developmental Editing** - Automated high-level structural improvements  

---

## 🚀 Quick Start

```powershell
# Install
git clone https://github.com/yourusername/libriscribe.git
cd libriscribe
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your GOOGLE_AI_STUDIO_API_KEY

# Run
libriscribe start
```

---

## 💡 How It Works

### 1. Write Your Book
```
> Create a new project
> Define characters, world, and plot
> Generate chapters automatically
```

### 2. Analyze with Professional Tools
```
> Export to AutoCrit, ProWritingAid, or Marlowe
> Get professional editorial feedback
```

### 3. Automated Developmental Editing
```
> Place reports in project/Autocrit/ folder
> Director Mode: "analyze reports in Autocrit"
> Review the generated action plan
> Director Mode: "execute the action plan" (coming soon!)
```

### 4. Creative Control
```
Director Mode commands:

> Make M a man
> Make Sarah 10 years older  
> Fix pronouns for Bond
> The heist should fail in Chapter 5
```

---

## 🎬 Director Agent

**Natural language interface for creative control**

Instead of manually editing files, just tell the AI what you want:

```
> Make the villain more sympathetic
✓ Updated characters.json
✓ Updated outline.md  
✓ Rewrote chapters 3, 5, 7
✓ Complete consistency maintained
```

**Supported Commands:**
- Character changes (gender, age, appearance, personality)
- Grammar corrections
- Pronoun fixing (context-aware)
- Report analysis
- Plot modifications (coming soon)

---

## 📊 Report Analyzer

**Analyzes editorial reports from any tool**

**Supported Formats:**
- PDF (with chart/graph analysis)
- DOCX (with embedded image analysis)
- RTF, TXT, MD

**Workflow:**
1. Export reports from AutoCrit/ProWritingAid/Marlowe
2. Place in `project/Autocrit/` folder
3. Run: `analyze reports in Autocrit`
4. Get actionable editorial plan with:
   - Major issues (high priority)
   - Minor issues (medium priority)
   - Strengths
   - Recommended actions

**Vision Analysis:**
- Analyzes pacing charts
- Extracts data from dialogue balance graphs
- Interprets visual feedback
- Includes insights in action plan

---

## 🏗️ Architecture

```
Director Agent
    ↓
Intent Parser → Impact Analyzer → Change Handlers
    ↓
Autonomous Project-Wide Modifier
    ↓
Updates ALL Files (characters, outline, scenes, chapters)
```

**Key Components:**
- **Director Agent** - Natural language interface
- **Autonomous Modifier** - LLM-powered consistency engine
- **Report Analyzer** - Professional feedback integration
- **Document Reader** - Universal format support
- **Vision Analysis** - Chart/graph interpretation

---

## 📦 Installation

### Prerequisites
- Python 3.13+
- Google AI Studio API key (free tier available)

### Required Dependencies
```powershell
pip install -r requirements.txt
```

### Optional (for full document support)
```powershell
# DOCX with images
pip install python-docx Pillow

# PDF support
pip install PyPDF2 pdf2image

# Better RTF parsing
pip install striprtf
```

### Poppler (Windows - for PDF image analysis)
1. Download: [Poppler Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract to `C:\poppler`
3. Add to PATH: `C:\poppler\Library\bin`

---

## 🎯 Use Cases

### Fiction Writers
- Generate complete novels from outline
- Maintain character consistency
- Automated developmental editing
- Professional-grade quality control

### Non-Fiction Authors
- Structure complex topics
- Consistent terminology
- Research integration
- Citation management

### Content Creators
- Rapid prototyping
- A/B testing different approaches
- Style consistency
- Automated editing

---

## 🔮 Roadmap

### v2.3 ✅ (Current Release - Dec 2025)
- [x] Style Presets System (Spy Maker, Epic Romance, etc.)
- [x] Story Structure Frameworks (Hero's Journey, Save the Cat, etc.)
- [x] Custom preset support
- [x] Automatic style injection into prompts

### v2.4 (Next Release)
- [ ] Execute Action Plan (auto-apply recommendations)
- [ ] Refine Action Plan (iterative feedback)
- [ ] Preview mode (show changes before applying)
- [ ] CLI commands for preset management

### v2.5
- [ ] Plot modification commands
- [ ] Worldbuilding changes
- [ ] Tone/style adjustments
- [ ] Undo/redo capability

### v3.0
- [ ] EditScribe integration
- [ ] Multi-user collaboration
- [ ] Version control
- [ ] Quality metrics dashboard

---

## 📊 Performance

**Typical Costs (Gemini 2.0 Flash):**
- Write chapter: $0.05-$0.15
- Review & edit: $0.03-$0.08
- Analyze reports: $0.20-$0.50
- Full book (15 chapters): $2-$5

**Speed:**
- Chapter generation: 2-5 minutes
- Report analysis: 3-8 minutes
- Full book: 2-4 hours

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas for contribution:**
- New change handlers
- Additional LLM providers
- Document format support
- Quality improvements
- Documentation

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- Google AI Studio for Gemini API
- OpenAI for GPT models
- Anthropic for Claude
- The open-source community

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/libriscribe/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/libriscribe/discussions)
- **Email:** support@libriscribe.com

---

## ⭐ Star History

If you find Libriscribe useful, please star the repository!

---

**Built with ❤️ by Fernando Guerra**

*Libriscribe - Where AI meets professional editing*
