# src/libriscribe/main.py
# Shakespeare AI - AI-Powered Book Creation
# Based on Libriscribe by Fernando Guerra
import sys
import typer
from libriscribe.agents.project_manager import ProjectManagerAgent
from typing import List, Dict, Any
from libriscribe.utils.llm_client import LLMClient
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import logging
import warnings
from pydantic import PydanticDeprecationWarning

from libriscribe.knowledge_base import ProjectKnowledgeBase, Chapter  # Import the new class
from libriscribe.settings import Settings
from rich.progress import track  # Import track
warnings.filterwarnings("ignore", category=PydanticDeprecationWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("shakespeare.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
for handler in logging.root.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(logging.Formatter("%(message)s"))
        handler.stream.reconfigure(errors='replace')

console = Console()
app = typer.Typer()
#project_manager = ProjectManagerAgent()  # Initialize ProjectManager
project_manager = ProjectManagerAgent(llm_client=None)
logger = logging.getLogger(__name__)

def select_llm(project_knowledge_base: ProjectKnowledgeBase): 
    """Lets the user select an LLM provider."""
    available_llms = []
    settings = Settings()

    if settings.openrouter_api_key:
        available_llms.append("openrouter")
    if settings.openai_api_key:
        available_llms.append("openai")
    if settings.claude_api_key:
        available_llms.append("claude")
    if settings.google_ai_studio_api_key:
        available_llms.append("google_ai_studio")
    if settings.deepseek_api_key:
        available_llms.append("deepseek")
    if settings.mistral_api_key:
        available_llms.append("mistral")

    if not available_llms:
        console.print("[red]❌ No LLM API keys found in .env file. Please add at least one.[/red]")
        raise typer.Exit(code=1)

    console.print("")
    llm_choice = select_from_list("🤖 Select your preferred AI model:", available_llms)
    
    # Convert display name back to API identifier
    if "OpenAI" in llm_choice:
        llm_choice = "openai"
    elif "Claude" in llm_choice:
        llm_choice = "claude"
    elif "Google Gemini" in llm_choice:
        llm_choice = "google_ai_studio"
    elif "DeepSeek" in llm_choice:
        llm_choice = "deepseek"
    elif "Mistral" in llm_choice:
        llm_choice = "mistral"
        
    project_knowledge_base.set("llm_provider", llm_choice)
    
    # If Google AI Studio, ask for Test/Production mode
    if llm_choice == "google_ai_studio":
        console.print("\n[bold cyan]🎯 Select LLM Mode:[/bold cyan]")
        console.print("[cyan]1.[/cyan] Test Mode (gemini-2.0-flash - Stable)")
        console.print("[cyan]2.[/cyan] Production Mode (gemini-2.0-flash-exp - Latest)")
        mode_choice = typer.prompt("Enter your choice", default="1").strip()
        
        if mode_choice == "2":
            app_env = "production"
            console.print("[green]✅ Production mode selected (High Quality)[/green]")
        else:
            app_env = "development"
            console.print("[green]✅ Test mode selected (Fast & Cheap)[/green]")
        
        # Update .env file
        import os
        from pathlib import Path
        env_path = Path(".env")
        if env_path.exists():
            lines = env_path.read_text().splitlines()
            # Remove existing APP_ENV line
            lines = [l for l in lines if not l.startswith("APP_ENV=")]
            # Add new APP_ENV line
            lines.append(f"APP_ENV={app_env}")
            env_path.write_text("\n".join(lines))
        else:
            env_path.write_text(f"APP_ENV={app_env}")
    
    return llm_choice

def introduction():
    """Prints a welcome message."""
    
    console.print("")
    console.print("")
    console.print("")   
    console.print(
        Panel(
            "Welcome to [bold]🎭 Shakespeare AI[/bold]! ✨\n\n"
            "An AI-powered book creation system for bringing your stories to life.\n\n"
            "🚀  Ready to write your next masterpiece?\n\n"
            "⭐ Star us on GitHub: [link]https://github.com/robertmonroe/shakespeare-ai[/link]\n"
            "🙏 Based on Libriscribe by Fernando Guerra",
            title="[bold blue]Shakespeare AI v2.3.0[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
    )
    # Print emojis separately to avoid formatting issues (Optional in this case)
    console.print("")
    console.print("")
    # Print emojis separately to avoid formatting issues
    console.print("Let's create something amazing! \n")

def select_from_list(prompt: str, options: List[str], allow_custom: bool = False) -> str:
    """Presents options and returns selection with improved formatting."""
    console.print(f"[bold]{prompt}[/bold]")
    
    # Display options with numbers
    for i, option in enumerate(options):
        console.print(f"[cyan]{i + 1}.[/cyan] {option}")
    
    if allow_custom:
        console.print(f"[cyan]{len(options) + 1}.[/cyan]Custom (enter your own)")
    
    # Get user selection with error handling
    while True:
        try:
            choice = typer.prompt("Enter your choice", show_choices=False)
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(options):
                return options[choice_idx]  # Return original option without emoji
            elif allow_custom and choice_idx == len(options):
                custom_value = typer.prompt("Enter your custom value")
                return custom_value
            else:
                console.print("[red]Invalid choice. Please try again.[/red]")
        except ValueError:
            console.print("[red]Please enter a number.[/red]")


def save_project_data():
    """Saves project data (using new method)."""
    project_manager.save_project_data() # Now it's the same


def generate_questions_with_llm(category: str, genre: str) -> Dict[str, Any]:
    """Generates genre-specific questions with improved error handling."""
    prompt = f"""
    Generate a list of 5-7 KEY questions that would help develop a {category} {genre} book.
    Format your response as a JSON object where keys are question IDs and values are the questions.
    
    For example:
    {{
        "q1": "What is the central conflict of your story?",
        "q2": "Who is the main antagonist?",
        "q3": "What is the world's primary magic system?"
    }}
    
    Return ONLY valid JSON, nothing else.
    """
    
    llm_client = project_manager.llm_client
    if llm_client is None:
        console.print("[red]LLM is not selected[/red]")
        return {}

    try:
        response = llm_client.generate_content(prompt, max_tokens=500)
        
        # Clean the response - find JSON content
        response = response.strip()
        # Look for JSON between curly braces if there's other text
        if '{' in response and '}' in response:
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
        else:
            json_str = response
            
        try:
            questions = json.loads(json_str)
            return questions
        except json.JSONDecodeError:
            # If it fails, create a minimal set of questions as fallback
            console.print("[yellow]Could not parse LLM response. Using default questions.[/yellow]")
            return {
                "q1": f"What key themes do you want to explore in your {genre} story?",
                "q2": "Who is your favorite character and why?",
                "q3": "What makes your story unique compared to similar works?"
            }
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        console.print(f"[yellow]Error generating custom questions. Using defaults.[/yellow]")
        return {
            "q1": f"What key themes do you want to explore in your {genre} story?",
            "q2": "Who is your favorite character and why?",
            "q3": "What makes your story unique compared to similar works?"
        }


# --- Helper functions for Simple Mode ---

def get_project_name_and_title():
    console.print("")
    project_name = typer.prompt("📁 Enter a project name (this will be the directory name)")
    console.print("")
    title = typer.prompt("📕 What is the title of your book?")
    return project_name, title

def get_category_and_genre(project_knowledge_base: ProjectKnowledgeBase):
    console.print("")
    category = select_from_list(
        "📚 What category best describes your book?",
        ["Fiction", "Non-Fiction", "Business", "Research Paper"],
        allow_custom=True,
    )
    project_knowledge_base.set("category", category)

    if category == "Fiction":
        genre_options = ["Fantasy", "Science Fiction", "Romance", "Thriller", "Mystery", "Historical Fiction", "Horror", "Young Adult", "Contemporary"]
    elif category == "Non-Fiction":
        genre_options = ["Biography", "History", "Science", "Self-Help", "Travel", "True Crime", "Cookbook"]
    elif category == "Business":
        genre_options = ["Marketing", "Management", "Finance", "Entrepreneurship", "Leadership", "Sales", "Productivity"]
    elif category == "Research Paper":
        genre = typer.prompt("🔬 Enter the field of study for your research paper")
        project_knowledge_base.set("genre", genre)
        return
    else:
        genre_options = []  # Should not happen, but for safety

    if genre_options:
        console.print("")
        genre = select_from_list(f"🏷️ What genre/subject best fits your {category} book?", genre_options, allow_custom=True)
        project_knowledge_base.set("genre", genre)



def get_book_length(project_knowledge_base: ProjectKnowledgeBase): 
    console.print("")
    book_length = select_from_list(
        "📏 How long would you like your book to be?",
        ["Short Story (1-3 chapters)", "Novella (5-8 chapters)", "Novel (15+ chapters)", "Full Book (Non-Fiction)"],
        allow_custom=False,
    )
    project_knowledge_base.set("book_length", book_length)

def get_fiction_details(project_knowledge_base: ProjectKnowledgeBase): 
    if project_knowledge_base.category == "Fiction":
        console.print("")
        num_characters = typer.prompt("👥 How many main characters will your story have?", type=int)
        project_knowledge_base.set("num_characters", num_characters)
        console.print("")
        worldbuilding_needed = typer.confirm("🌍 Does your story require extensive worldbuilding?")
        project_knowledge_base.set("worldbuilding_needed", worldbuilding_needed)

def get_review_preference(project_knowledge_base: ProjectKnowledgeBase): 
    console.print("")
    review_preference = select_from_list("📝 How would you like your chapters to be reviewed?", ["Human (you'll review it)", "AI (automatic review)"])
    project_knowledge_base.set("review_preference", review_preference)
    
    # If AI review, ask for manual or auto mode
    if "AI" in review_preference or "automatic" in review_preference.lower():
        console.print("\n[cyan]AI Review Mode[/cyan]")
        review_mode = select_from_list(
            "Choose review mode",
            ["Manual (interactive - you control each pass)", "Auto (automated - runs configured passes)"]
        )
        
        # Store the mode choice
        is_auto_mode = "Auto" in review_mode or "automated" in review_mode.lower()
        project_knowledge_base.set("auto_review_mode", is_auto_mode)
        
        if is_auto_mode:
            console.print("\n[cyan]Auto-Review Configuration[/cyan]")
            console.print("[yellow]How many automated review/edit passes per chapter?[/yellow]")
            console.print("  • Recommended: 15-20 passes for most chapters")
            console.print("  • Range: 1-30 passes")
            console.print("  • Each pass takes ~6 minutes")
            
            while True:
                auto_passes = typer.prompt("\nNumber of passes (1-30)", type=int)
                
                if 1 <= auto_passes <= 30:
                    project_knowledge_base.set("auto_review_passes", auto_passes)
                    est_minutes = auto_passes * 6
                    est_hours = est_minutes / 60
                    if est_hours >= 1:
                        console.print(f"[cyan]⏱️  Estimated time per chapter: ~{est_hours:.1f} hours ({est_minutes} min)[/cyan]")
                    else:
                        console.print(f"[cyan]⏱️  Estimated time per chapter: ~{est_minutes} minutes[/cyan]")
                    break
                else:
                    console.print("[red]❌ Invalid range. Please enter 1-30.[/red]")
        else:
            # Manual mode - set passes to 0 (user controls)
            project_knowledge_base.set("auto_review_passes", 0)

def get_description(project_knowledge_base: ProjectKnowledgeBase): 
    console.print("")
    description = typer.prompt("📝 Provide a brief description of your book's concept or plot")
    project_knowledge_base.set("description", description)
    
    # Concept generation toggles
    console.print("")
    console.print("[yellow]⚙️  Concept Generation Options:[/yellow]")
    console.print("The AI can critique and refine your description, or use it exactly as written.")
    console.print("")
    
    skip_critique = typer.confirm("Skip concept critique? (Use your description without AI evaluation)", default=False)
    project_knowledge_base.skip_concept_critique = skip_critique
    
    skip_refinement = typer.confirm("Skip concept refinement? (Use your description without AI rewriting)", default=False)
    project_knowledge_base.skip_concept_refinement = skip_refinement
    
    if skip_critique and skip_refinement:
        console.print("[green]✓ Your exact description will be used without changes[/green]")
    elif skip_critique:
        console.print("[yellow]⚠ Your description will be refined but not critiqued[/yellow]")
    elif skip_refinement:
        console.print("[yellow]⚠ Your description will be critiqued but not refined[/yellow]")
    else:
        console.print("[cyan]ℹ Your description will go through full critique and refinement[/cyan]")

def generate_and_review_concept(project_knowledge_base: ProjectKnowledgeBase): 
    project_manager.generate_concept()
    project_manager.checkpoint() # Checkpoint
    console.print("")
    console.print(f"\n[cyan]✨ Refined Concept:[/cyan]")
    console.print(f"  [bold]Title:[/bold] {project_knowledge_base.title}")
    console.print(f"  [bold]Logline:[/bold] {project_knowledge_base.logline}")
    console.print(f"  [bold]Description:[/bold]\n{project_knowledge_base.description}")
    return typer.confirm("Do you want to proceed with generating an outline based on this concept?")

def generate_and_edit_outline(project_knowledge_base: ProjectKnowledgeBase): 
    project_manager.generate_outline()
    project_manager.checkpoint()  # Checkpoint after outline
    console.print("")
    console.print(f"\n[green]📋 Outline generated![/green]")

    if typer.confirm("Do you want to review and edit the outline now?"):
        typer.edit(filename=str(project_manager.project_dir / "outline.md"))
        print("\nChanges saved.")


def generate_characters_if_needed(project_knowledge_base: ProjectKnowledgeBase): 
     if project_knowledge_base.get("num_characters", 0) > 0:  # Use get with default
        console.print("")
        if typer.confirm("Do you want to generate character profiles?"):
            console.print("\n[cyan]👥 Generating character profiles...[/cyan]")
            project_manager.generate_characters()
            project_manager.checkpoint() # Checkpoint
            console.print("")
            console.print(f"\n[green]✅ Character profiles generated![/green]")

def generate_worldbuilding_if_needed(project_knowledge_base: ProjectKnowledgeBase): 
    if project_knowledge_base.get("worldbuilding_needed", False):  # Use get with default
        console.print("")
        if typer.confirm("Do you want to generate worldbuilding details?"):
            console.print("\n[cyan]🗺️ Creating worldbuilding details...[/cyan]")
            project_manager.generate_worldbuilding()
            project_manager.checkpoint() # Checkpoint
            console.print("")
            console.print(f"\n[green]✅ Worldbuilding details generated![/green]")

def write_and_review_chapters(project_knowledge_base: ProjectKnowledgeBase):
    """Write and review chapters with better progress tracking and error handling."""
    num_chapters = project_knowledge_base.get("num_chapters", 1)
    if isinstance(num_chapters, tuple):
        num_chapters = num_chapters[1]

    console.print(f"\n[bold]Starting chapter writing process. Total chapters: {num_chapters}[/bold]")
    
    # Determine if using AI review for automatic processing
    using_ai_review = project_knowledge_base.get("review_preference", "") == "AI"
    
    # If using AI review, ask once if they want to proceed with all chapters
    if using_ai_review and num_chapters > 1:
        if not typer.confirm(f"\nAI will automatically write and review all {num_chapters} chapters. Proceed?"):
            return
    
    for i in range(1, num_chapters + 1):
        chapter = project_knowledge_base.get_chapter(i)
        if chapter is None:
            console.print(f"[yellow]WARNING: Chapter {i} not found in outline. Creating basic structure...[/yellow]")
            chapter = Chapter(
                chapter_number=i,
                title=f"Chapter {i}",
                summary="To be written"
            )
            project_knowledge_base.add_chapter(chapter)  # Add to knowledge base!

        console.print(f"\n[cyan]Writing Chapter {i}: {chapter.title}[/cyan]")

        if project_manager.does_chapter_exist(i):
            # If using AI review, automatically overwrite existing chapters
            # Otherwise, ask for confirmation
            if not using_ai_review and not typer.confirm(f"Chapter {i} already exists. Overwrite?"):
                console.print(f"[yellow]Skipping chapter {i}...[/yellow]")
                continue

        try:
            project_manager.write_and_review_chapter(i)
            project_manager.checkpoint()
            console.print("")
            console.print(f"[green]✅ Chapter {i} completed successfully[/green]")
        except Exception as e:
            console.print(f"[red]ERROR writing chapter {i}: {str(e)}[/red]")
            logger.exception(f"Error writing chapter {i}")
            if not using_ai_review and not typer.confirm("Continue with next chapter?"):
                break

        # Only ask to continue if NOT using AI review and there are more chapters
        if i < num_chapters and not using_ai_review:
            if not typer.confirm("\nContinue to next chapter?"):
                break

    console.print("\n[green]Chapter writing process completed![/green]")

def format_book(project_knowledge_base: ProjectKnowledgeBase): 
    console.print("")
    if typer.confirm("Do you want to format the book now?"):
        output_format = select_from_list("Choose output format:", ["Markdown (.md)", "PDF (.pdf)"])
        if output_format == "Markdown (.md)":
            output_path = str(project_manager.project_dir / "manuscript.md")
        else:
            output_path = str(project_manager.project_dir / "manuscript.pdf")
        project_manager.format_book(output_path)
        console.print("")
        console.print(f"\n[green]📘 Book formatted and saved![/green]")


# --- Simple Mode (Refactored) ---
def simple_mode():
    console.print("\n[cyan]✨ Starting Simple Mode...[/cyan]\n")

    project_name, title = get_project_name_and_title()
    project_knowledge_base = ProjectKnowledgeBase(project_name=project_name, title=title)

    # Add language selection right after project name and title
    select_language(project_knowledge_base)
    
    llm_choice = select_llm(project_knowledge_base)
    project_manager.initialize_llm_client(llm_choice)

    get_category_and_genre(project_knowledge_base)
    get_book_length(project_knowledge_base)
    get_fiction_details(project_knowledge_base)
    get_review_preference(project_knowledge_base)
    get_description(project_knowledge_base)

    project_manager.initialize_project_with_data(project_knowledge_base)

    if generate_and_review_concept(project_knowledge_base):
        generate_and_edit_outline(project_knowledge_base)
        generate_characters_if_needed(project_knowledge_base)
        generate_worldbuilding_if_needed(project_knowledge_base)

        project_manager.checkpoint() 
        # Ensure chapters are written
        num_chapters = project_knowledge_base.get("num_chapters", 1)
        if isinstance(num_chapters, tuple):
            num_chapters = num_chapters[1]

        print(f"\nPreparing to write {num_chapters} chapters...")

        # Determine if using AI review for automatic processing
        using_ai_review = project_knowledge_base.get("review_preference", "") == "AI"

        # If using AI review, ask once if they want to proceed with all chapters
        if using_ai_review and num_chapters > 1:
            if typer.confirm(f"AI will automatically write and review all {num_chapters} chapters. Proceed?"):
                # Write all chapters automatically
                for chapter_num in range(1, num_chapters + 1):
                    project_manager.write_and_review_chapter(chapter_num)
                    project_manager.checkpoint()
        else:
            # User interaction for each chapter
            for chapter_num in range(1, num_chapters + 1):
                if not typer.confirm(f"\n📝 Ready to write Chapter {chapter_num}?"):
                    break
                project_manager.write_and_review_chapter(chapter_num)
                project_manager.checkpoint()

        # Only format after chapters are written
        if typer.confirm("\nDo you want to format the book now?"):
            format_book(project_knowledge_base)
    else:
        print("Exiting.")
        return

    console.print("\n[green]🎉 Book creation process complete![/green]")

# --- Helper Functions for Advanced Mode ---

def get_advanced_fiction_details(project_knowledge_base: ProjectKnowledgeBase):
    """Gets detailed information for fiction projects with proper type conversion."""
    console.print("")
    num_characters_str = typer.prompt(
        "👥 How many main characters do you envision? (e.g., 3, 2-4, 5+)", default="2-3"
    )
    project_knowledge_base.set("num_characters_str", num_characters_str)
    
    # Convert to appropriate type
    if "-" in num_characters_str:
        try:
            min_val, max_val = map(int, num_characters_str.split("-"))
            project_knowledge_base.set("num_characters", (min_val, max_val))
        except ValueError:
            # Fallback if conversion fails
            project_knowledge_base.set("num_characters", (2, 3))
    elif "+" in num_characters_str:
        try:
            base_val = int(num_characters_str.replace("+", ""))
            project_knowledge_base.set("num_characters", base_val)
        except ValueError:
            project_knowledge_base.set("num_characters", 3)
    else:
        try:
            project_knowledge_base.set("num_characters", int(num_characters_str))
        except ValueError:
            # Fallback if conversion fails
            project_knowledge_base.set("num_characters", 3)

    console.print("")
    worldbuilding_needed = typer.confirm("🌍 Does your story need extensive worldbuilding?")
    project_knowledge_base.set("worldbuilding_needed", worldbuilding_needed)

    console.print("")
    tone = select_from_list("🎭 What overall tone would you like for your book?", 
                     ["Serious", "Funny", "Romantic", "Informative", "Persuasive"])
    
    project_knowledge_base.set("tone", tone)

    console.print("")
    target_audience = select_from_list("👥 Who is your target audience?", 
                             ["Children", "Teens", "Young Adult", "Adults"])
    project_knowledge_base.set("target_audience", target_audience)

    console.print("")
    book_length = select_from_list(
        "📏 How long will your book be?",
        ["Short Story", "Novella", "Novel", "Full Book"],
        allow_custom=False,
    )
    project_knowledge_base.set("book_length", book_length)

    console.print("")
    num_chapters_str = typer.prompt(
        "🔢 Approximately how many chapters do you want? (e.g., 10, 8-12, 20+)",
        default="8-12"
    )
    project_knowledge_base.set("num_chapters_str", num_chapters_str)
    
    # Convert to appropriate type
    if "-" in num_chapters_str:
        try:
            min_val, max_val = map(int, num_chapters_str.split("-"))
            project_knowledge_base.set("num_chapters", (min_val, max_val))
        except ValueError:
            # Fallback if conversion fails
            project_knowledge_base.set("num_chapters", (8, 12))
    elif "+" in num_chapters_str:
        try:
            base_val = int(num_chapters_str.replace("+", ""))
            project_knowledge_base.set("num_chapters", base_val)
        except ValueError:
            project_knowledge_base.set("num_chapters", 12)
    else:
        try:
            project_knowledge_base.set("num_chapters", int(num_chapters_str))
        except ValueError:
            # Fallback if conversion fails
            project_knowledge_base.set("num_chapters", 10)
            
    inspired_by = typer.prompt("✨ Are there any authors, books, or series that inspire you? (Optional)")
    project_knowledge_base.set("inspired_by", inspired_by)

def get_advanced_nonfiction_details(project_knowledge_base: ProjectKnowledgeBase): 
    project_knowledge_base.set("num_characters", 0)
    project_knowledge_base.set("num_chapters",0)
    project_knowledge_base.set("worldbuilding_needed",False)

    console.print("")
    tone = select_from_list("🎭 What tone would you like for your non-fiction book?", 
                    ["Serious", "Funny", "Romantic", "Informative", "Persuasive"])
    project_knowledge_base.set("tone", tone)

    console.print("")
    target_audience = select_from_list(
        "👥 Who is your target audience?",
        ["Children", "Teens", "Young Adult", "Adults", "Professional/Expert"],
    )
    project_knowledge_base.set("target_audience", target_audience)

    console.print("")
    book_length = select_from_list(
        "Select the desired book length:",
        ["Article", "Essay", "Full Book"],
        allow_custom=False,
    )
    project_knowledge_base.set("book_length", book_length)

    console.print("")
    author_experience = typer.prompt("🧠 What is your experience or expertise in this subject?")
    project_knowledge_base.set("author_experience",author_experience)

def get_advanced_business_details(project_knowledge_base: ProjectKnowledgeBase): 
    project_knowledge_base.set("num_characters",0)
    project_knowledge_base.set("num_chapters",0)
    project_knowledge_base.set("worldbuilding_needed",False)

    console.print("")
    tone = select_from_list("Select Tone", ["Informative", "Motivational", "Instructive"])
    project_knowledge_base.set("tone", tone)

    console.print("")
    target_audience = select_from_list(
        "👥 Select Target Audience",
        [
            "Entrepreneurs",
            "Managers",
            "Employees",
            "Students",
            "General Business Readers",
        ],
    )
    project_knowledge_base.set("target_audience", target_audience)

    console.print("")
    book_length = select_from_list(
        "📏 Select the desired book length:",
        ["Pamphlet", "Guidebook", "Full Book"],
        allow_custom=False,
    )
    project_knowledge_base.set("book_length", book_length)

    console.print("")
    key_takeaways = typer.prompt("What are the key takeaways you want readers to gain?")
    project_knowledge_base.set("key_takeaways",key_takeaways)

    console.print("")
    case_studies = typer.confirm("Will you include case studies?")
    project_knowledge_base.set("case_studies", case_studies)

    console.print("")
    actionable_advice = typer.confirm("Will you provide actionable advice/exercises?")
    project_knowledge_base.set("actionable_advice",actionable_advice)

    if project_knowledge_base.get("genre") == "Marketing":
        
        console.print("")
        marketing_focus = select_from_list(
            "✨ What is the primary focus of your marketing book?",
            [
                "SEO",
                "Performance Marketing",
                "Data Analytics",
                "Offline Marketing",
                "Content Marketing",
                "Social Media Marketing",
                "Branding",
            ],
            allow_custom=True,
        )
        project_knowledge_base.set("marketing_focus",marketing_focus)

    elif project_knowledge_base.get("genre") == "Sales":
        console.print("")
        sales_focus = select_from_list(
            "✨  What is the primary focus of your sales book?",
            [
                "Sales Techniques",
                "Pitching",
                "Negotiation",
                "Building Relationships",
                "Sales Management",
            ],
            allow_custom=True,
        )
        project_knowledge_base.set("sales_focus", sales_focus)

def get_advanced_research_details(project_knowledge_base: ProjectKnowledgeBase): 
    project_knowledge_base.set("num_characters",0)
    project_knowledge_base.set("num_chapters",0)
    project_knowledge_base.set("worldbuilding_needed",False)
    project_knowledge_base.set("tone","Formal and Objective")

    console.print("")
    target_audience = select_from_list(
        "👥 Select Target Audience",
        ["Academic Community", "Researchers", "Students", "General Public (if applicable)"],
    )
    console.print("")
    project_knowledge_base.set("target_audience", target_audience)

    console.print("")
    project_knowledge_base.set("book_length","Academic Article")

    console.print("")
    research_question = typer.prompt("What is your primary research question?")
    project_knowledge_base.set("research_question",research_question)

    console.print("")
    hypothesis = typer.prompt("What is your hypothesis (if applicable)?")
    project_knowledge_base.set("hypothesis", hypothesis)

    console.print("")
    methodology = select_from_list(
        "📊 Select your research methodology:",
        ["Quantitative", "Qualitative", "Mixed Methods"],
        allow_custom=True,
    )
    project_knowledge_base.set("methodology", methodology)

def get_dynamic_questions(project_knowledge_base: ProjectKnowledgeBase): 
    print("\nNow, let's dive into some genre-specific questions...")
    dynamic_questions = generate_questions_with_llm(project_knowledge_base.get("category"), project_knowledge_base.get("genre"))

    for q_id, question in dynamic_questions.items():
        answer = typer.prompt(question)
        project_knowledge_base.dynamic_questions[q_id] = answer
        save_project_data()

# --- Advanced Mode (Refactored with Submenu) ---

def advanced_mode():
    """Advanced mode with submenu for create/manage/exit."""
    console.print("\n[cyan]✨ Starting Advanced Mode...[/cyan]\n")
    
    while True:
        # Show the submenu
        console.print("[bold]What would you like to do?[/bold]")
        console.print("[cyan]1.[/cyan] Create new project")
        console.print("[cyan]2.[/cyan] Manage existing project")
        console.print("[cyan]3.[/cyan] Exit")

        choice = typer.prompt("Enter your choice", show_choices=False)

        if choice == "1":
            create_new_advanced_project()
        elif choice == "2":
            manage_existing_project()
        elif choice == "3":
            break
        else:
            console.print("[red]Invalid choice.[/red]")


def create_new_advanced_project():
    """Creates a new project in advanced mode."""
    project_name, title = get_project_name_and_title()
    project_knowledge_base = ProjectKnowledgeBase(project_name=project_name, title=title) 

    select_language(project_knowledge_base)
    llm_choice = select_llm(project_knowledge_base) 
    project_manager.initialize_llm_client(llm_choice)

    get_category_and_genre(project_knowledge_base) 

    if project_knowledge_base.get("category") == "Fiction":
        get_advanced_fiction_details(project_knowledge_base) 
    elif project_knowledge_base.get("category") == "Non-Fiction":
        get_advanced_nonfiction_details(project_knowledge_base) 
    elif project_knowledge_base.get("category") == "Business":
        get_advanced_business_details(project_knowledge_base) 
    elif project_knowledge_base.get("category") == "Research Paper":
        get_advanced_research_details(project_knowledge_base) 

    get_review_preference(project_knowledge_base) 
    get_description(project_knowledge_base) 

    project_manager.initialize_project_with_data(project_knowledge_base)
    get_dynamic_questions(project_knowledge_base) 

    if generate_and_review_concept(project_knowledge_base): 
        generate_and_edit_outline(project_knowledge_base) 
        generate_characters_if_needed(project_knowledge_base) 
        generate_worldbuilding_if_needed(project_knowledge_base) 
        write_and_review_chapters(project_knowledge_base)
        format_book(project_knowledge_base)
    else:
        console.print("[yellow]Exiting.[/yellow]")
        return

    console.print("\n[green]🎉 Book creation process complete (Advanced Mode)![/green]")


def manage_existing_project():
    """Manages an existing project - lists available projects and loads one."""
    import os
    
    # List available projects
    projects_dir = "projects"  # Adjust this to your actual projects directory
    if not os.path.exists(projects_dir):
        console.print("[red]❌ No projects directory found.[/red]")
        return
    
    projects = [d for d in os.listdir(projects_dir) 
                if os.path.isdir(os.path.join(projects_dir, d))]
    
    if not projects:
        console.print("[yellow]No existing projects found.[/yellow]")
        return
    
    console.print("\n[bold]Available Projects:[/bold]")
    for i, proj in enumerate(projects, 1):
        console.print(f"[cyan]{i}.[/cyan] {proj}")
    
    console.print("")
    project_choice = typer.prompt("Enter project number to manage", show_choices=False).strip()
    
    try:
        project_idx = int(project_choice) - 1
        if 0 <= project_idx < len(projects):
            project_name = projects[project_idx]
            console.print(f"\n[green]Loading project: {project_name}[/green]")
            
            try:
                # Load project data
                project_manager.load_project_data(project_name)
                
                # CRITICAL: Initialize LLM client with the saved provider
                if project_manager.project_knowledge_base:
                    llm_provider = project_manager.project_knowledge_base.get("llm_provider", "openai")
                    console.print(f"[cyan]Initializing AI model ({llm_provider})...[/cyan]")
                    project_manager.initialize_llm_client(llm_provider)
                
                console.print(f"[green]✅ Project '{project_name}' loaded successfully![/green]")
                
                # Show management options
                show_project_management_menu(project_name)
            except FileNotFoundError:
                console.print(f"[red]❌ Project '{project_name}' not found.[/red]")
            except ValueError as e:
                console.print(f"[red]❌ Error loading project: {e}[/red]")
        else:
            console.print("[red]❌ Invalid project number.[/red]")
    except ValueError:
        console.print("[red]❌ Please enter a valid number.[/red]")


def show_project_management_menu(project_name: str):
    """Shows options for managing an existing project."""
    while True:
        console.print(f"\n[bold]Managing Project: {project_name}[/bold]")
        console.print("[cyan]1.[/cyan] Resume writing")
        console.print("[cyan]2.[/cyan] Edit outline")
        console.print("[cyan]3.[/cyan] Regenerate characters")
        console.print("[cyan]4.[/cyan] Review existing chapter")
        console.print("[cyan]5.[/cyan] Format book")
        console.print("[cyan]6.[/cyan] Director Mode")
        console.print("[cyan]7.[/cyan] Back to main menu")
        console.print("")
        
        choice = typer.prompt("Enter your choice", show_choices=False).strip()
        
        if choice == "1":
            # Resume writing logic
            if not project_manager.project_knowledge_base:
                console.print("[red]❌ Project data not loaded.[/red]")
                continue
                
            num_chapters = project_manager.project_knowledge_base.get("num_chapters", 1)
            if isinstance(num_chapters, tuple):
                num_chapters = num_chapters[1]
            
            # Find last written chapter
            last_chapter = 0
            for i in range(1, num_chapters + 1):
                if project_manager.project_dir and (project_manager.project_dir / f"chapter_{i}.md").exists():
                    last_chapter = i
                else:
                    break
            
            remaining_chapters = num_chapters - last_chapter
            console.print(f"[cyan]Last written chapter: {last_chapter}[/cyan]")
            console.print(f"[cyan]Remaining chapters: {remaining_chapters}[/cyan]")
            
            # Ask about auto-write mode if more than 1 chapter remaining
            if remaining_chapters > 1:
                auto_write = typer.confirm(
                    f"\n🤖 Auto-write all {remaining_chapters} remaining chapters?",
                    default=False
                )
                
                if auto_write:
                    # Show summary
                    auto_passes = project_manager.project_knowledge_base.get("auto_review_passes", 25)
                    auto_mode = project_manager.project_knowledge_base.get("auto_review_mode", False)
                    
                    time_per_chapter = auto_passes * 6 if auto_mode else 30  # ~6 min per pass or 30 min manual
                    total_time = remaining_chapters * time_per_chapter
                    hours = total_time // 60
                    
                    console.print(f"\n[bold green]🤖 AUTO-WRITE MODE[/bold green]")
                    console.print(f"[cyan]Chapters: {last_chapter + 1} to {num_chapters} ({remaining_chapters} chapters)[/cyan]")
                    if auto_mode:
                        console.print(f"[cyan]Review passes per chapter: {auto_passes}[/cyan]")
                    console.print(f"[yellow]⏱️  Estimated time: ~{hours} hours ({time_per_chapter} min/chapter)[/yellow]")
                    console.print(f"\n[yellow]⚠️  This will run unattended. Press Ctrl+C to stop anytime.[/yellow]")
                    
                    if typer.confirm("\nReady to start?", default=True):
                        # AUTO-WRITE MODE
                        for i in range(last_chapter + 1, num_chapters + 1):
                            console.print(f"\n{'='*80}")
                            console.print(f"[bold cyan]📖 CHAPTER {i} of {num_chapters}[/bold cyan]")
                            console.print(f"{'='*80}\n")
                            
                            try:
                                project_manager.write_and_review_chapter(i)
                                console.print(f"\n[green]✅ Chapter {i} complete![/green]")
                            except KeyboardInterrupt:
                                console.print(f"\n[yellow]⚠️  Auto-write interrupted at Chapter {i}[/yellow]")
                                console.print(f"[cyan]Use 'Resume writing' to continue from Chapter {i}[/cyan]")
                                break
                            except Exception as e:
                                console.print(f"[red]❌ Error writing Chapter {i}: {str(e)}[/red]")
                                logger.exception(f"Error in auto-write for Chapter {i}")
                                if not typer.confirm("Continue with next chapter?", default=False):
                                    break
                        
                        console.print(f"\n[bold green]🎉 Auto-write complete![/bold green]")
                    else:
                        console.print("[yellow]Auto-write cancelled.[/yellow]")
                else:
                    # MANUAL MODE - write one chapter at a time
                    for i in range(last_chapter + 1, num_chapters + 1):
                        project_manager.write_and_review_chapter(i)
                        break  # Only write one chapter
            else:
                # Only 1 or 0 chapters remaining, just write it
                for i in range(last_chapter + 1, num_chapters + 1):
                    project_manager.write_and_review_chapter(i)
            
        elif choice == "2":
            if project_manager.project_dir:
                typer.edit(filename=str(project_manager.project_dir / "outline.md"))
                console.print("[green]✅ Outline edited.[/green]")
            
        elif choice == "3":
            project_manager.generate_characters()
            console.print("[green]✅ Characters regenerated.[/green]")
            
        elif choice == "4":
            # Review existing chapter
            if not project_manager.project_knowledge_base:
                console.print("[red]❌ Project data not loaded.[/red]")
                continue
            
            # Get chapter number
            chapter_num = typer.prompt("Enter chapter number to review", type=int)
            
            # Check if chapter exists
            if project_manager.project_dir:
                chapter_file = project_manager.project_dir / f"chapter_{chapter_num}.md"
                if not chapter_file.exists():
                    console.print(f"[red]❌ Chapter {chapter_num} not found![/red]")
                    continue
            
            # Get number of passes
            num_passes = typer.prompt("Enter number of review passes (1-30)", type=int)
            
            if num_passes < 1 or num_passes > 30:
                console.print("[red]❌ Passes must be between 1 and 30[/red]")
                continue
            
            # Confirm
            console.print(f"\n[cyan]Will run {num_passes} review/edit passes on Chapter {chapter_num}[/cyan]")
            if typer.confirm("Continue?", default=True):
                # Run review passes
                for pass_num in range(1, num_passes + 1):
                    console.print(f"\n🔄 [bold]Pass {pass_num} of {num_passes}[/bold]")
                    
                    # Review existing chapter (don't rewrite!)
                    console.print("[cyan]🔍 Reviewing...[/cyan]")
                    project_manager.chapter_flow_manager.review_chapter(chapter_num)
                    
                    # Edit based on review
                    console.print("[cyan]✏️  Editing...[/cyan]")
                    project_manager.chapter_flow_manager.edit_chapter(chapter_num)
                
                console.print(f"\n[green]✅ Chapter {chapter_num} review complete![/green]")
            
        elif choice == "5":
            if project_manager.project_knowledge_base:
                format_book(project_manager.project_knowledge_base)
            
        elif choice == "6":
            # Director Mode
            if project_manager.project_knowledge_base and project_manager.llm_client:
                from libriscribe.agents.director_agent import DirectorAgent
                
                director = DirectorAgent(
                    project_manager.llm_client,
                    project_manager.project_dir,
                    project_manager.project_knowledge_base
                )
                
                console.print("\n[bold cyan]🎬 Director Mode[/bold cyan]")
                console.print("[dim]Type your creative direction (or 'exit' to quit)[/dim]\n")
                
                while True:
                    command = typer.prompt(">", show_default=False).strip()
                    
                    if command.lower() in ['exit', 'quit', 'q']:
                        console.print("[yellow]Exiting Director Mode[/yellow]")
                        break
                    
                    if command:
                        director.execute(command)
                    
                    console.print("")  # Blank line for readability
            else:
                console.print("[red]❌ Project not loaded or LLM not initialized[/red]")
            
        elif choice == "7":
            break
        else:
            console.print("[red]❌ Invalid choice.[/red]")


def select_language(project_knowledge_base: ProjectKnowledgeBase):
    """Lets the user select a language for their book."""
    console.print("")
    language_options = [
        "English",
        "Spanish",
        "Brazilian Portuguese",
        "French",
        "German",
        "Chinese (Simplified)",
        "Japanese",
        "Russian",
        "Arabic",
        "Hindi"
    ]
    language = select_from_list("🌍 Select the language for your book:", language_options, allow_custom=True)
    project_knowledge_base.set("language", language)
    return language

@app.command()
def start():
    """Starts the interactive book creation process."""
    introduction()
    
    mode_options = ["Simple (guided process)", "Advanced (more options)"]
    mode = select_from_list("✨ Choose your creation mode:", mode_options)
    
    if "Simple" in mode:
        simple_mode()
    elif "Advanced" in mode:
        advanced_mode()


# Removed the create command

@app.command()
def outline():
    """Generates a book outline."""
    project_manager.generate_outline()

@app.command()
def characters():
    """Generates character profiles."""
    project_manager.generate_characters()

@app.command()
def worldbuilding():
    """Generates worldbuilding details."""
    project_manager.generate_worldbuilding()

@app.command()
def write(chapter_number: int = typer.Option(..., prompt="Chapter number")):
    """Writes a specific chapter, with review process."""
    logger.info(f"📝 Agent {project_manager.agents['chapter_writer'].name} writing chapter {chapter_number}...") # type: ignore
    project_manager.write_and_review_chapter(chapter_number)
    logger.info(f"✅ Chapter {chapter_number} complete.")



@app.command()
def edit(chapter_number: int = typer.Option(..., prompt="Chapter number to edit")):
    """Edits and refines a specific chapter"""
    project_manager.edit_chapter(chapter_number)


@app.command()
def format():
    """Formats the entire book into a single Markdown or PDF file."""
    output_format = select_from_list("Choose output format:", ["Markdown (.md)", "PDF (.pdf)"])
    if output_format == "Markdown (.md)":
        output_path = str(project_manager.project_dir / "manuscript.md")
    else:
        output_path = str(project_manager.project_dir / "manuscript.pdf")
    project_manager.format_book(output_path)  # Pass output_path here
    print(f"\nBook formatted and saved to: {output_path}")

@app.command()
def research(query: str = typer.Option(..., prompt="Research query")):
    """Performs web research on a given query."""
    project_manager.research(query)

@app.command()
def resume(project_name: str = typer.Option(..., prompt="Project name to resume")):
    """Resumes a project from the last checkpoint."""
    try:
        project_manager.load_project_data(project_name)
        print(f"Project '{project_name}' loaded. Resuming...")

        # Determine where to resume from.  This logic is simplified for now
        # and assumes you'll mostly resume chapter writing. A more robust
        # solution would inspect more files.

        if not project_manager.project_knowledge_base: 
            print("ERROR resuming project")
            return

        if project_manager.project_dir and (project_manager.project_dir / "outline.md").exists():
            # Find the last written chapter
            last_chapter = 0
            num_chapters = project_manager.project_knowledge_base.get("num_chapters",1) 
            if isinstance(num_chapters, tuple):
                num_chapters = num_chapters[1]

            for i in range(1, num_chapters + 1):  # Iterate in order
                if (project_manager.project_dir / f"chapter_{i}.md").exists():
                    last_chapter = i
                else:
                    break  # Stop at the first missing chapter

            print(f"Last written chapter: {last_chapter}")

            # Check the project data and files to determine next steps
            for i in range(last_chapter + 1, num_chapters + 1):
                 project_manager.write_and_review_chapter(i)
            if typer.confirm("Do you want to format now the book?"):
                format()

        elif project_manager.project_knowledge_base:  # Project data exists, but no outline 
            # Resume from outline generation (this is a simplification)
            print("Resuming from outline generation...")
            project_manager.generate_outline()
            # ... (rest of the logic, similar to simple/advanced mode)

        else:
            print("No checkpoint found to resume from.")


    except FileNotFoundError:
        print(f"Project '{project_name}' not found.")
    except ValueError as e:
        print(f"Error loading project data: {e}")



if __name__ == "__main__":
    # Display environment info for debugging
    if "--debug" in sys.argv:
        console.print("[yellow]Debug Info:[/yellow]")
        console.print(f"Python: {sys.version}")
        console.print(f"Terminal: {os.environ.get('TERM', 'Unknown')}")
        import rich
        console.print(f"Rich version: {rich.__version__}")
        # Then continue with normal app execution
    app()