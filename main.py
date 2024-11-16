import os
import arxiv
import pypdf
import argparse
from datetime import datetime
from colorama import Fore, Back, Style

def print_message_with_timestamp(message: str, color: str) -> None:
    """Prints a message with the current date and time in the specified color.

    Args:
        message (str): The message to print.
        color (str): The color formatting to apply to the message.

    Example usage:
        print_message_with_timestamp("This is a test message.", Fore.GREEN)
    """
    # Get the current date and time in the specified format
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print the message with the current time and the specified color
    # The color is applied before the message and reset after
    print(f"{color}{current_time} - {message}{Style.RESET_ALL}")

def success(message: str) -> None:
    """Prints a success message with black text and green highlight.

    Example usage:
        success("Operation completed successfully.")
    """
    # Call the print_message_with_timestamp function to print a success message
    # The message will be displayed in bright black text on a green background
    print_message_with_timestamp(message, f"{Style.BRIGHT}{Fore.BLACK}{Back.GREEN}")

def info(message: str) -> None:
    """Prints an info message with black text and cyan highlight.

    Example usage:
        info("This is an informational message.")
    """
    # Call the print_message_with_timestamp function to print an info message
    # The message will be displayed in bright black text on a cyan background
    print_message_with_timestamp(message, f"{Style.BRIGHT}{Fore.BLACK}{Back.CYAN}")

def warning(message: str) -> None:
    """Prints a warning message with black text and yellow highlight.

    Example usage:
        warning("This is a warning message.")
    """
    # Call the print_message_with_timestamp function to print a warning message
    # The message will be displayed in bright black text on a yellow background
    print_message_with_timestamp(message, f"{Style.BRIGHT}{Fore.BLACK}{Back.YELLOW}")

def error(message: str) -> None:
    """Prints an error message with bold white text and red highlight.

    Example usage:
        error("An error occurred during the operation.")
    """
    # Call the print_message_with_timestamp function to print an error message
    # The message will be displayed in bright white text on a red background
    print_message_with_timestamp(message, f"{Style.BRIGHT}{Fore.WHITE}{Back.RED}")

def parse_args() -> argparse.Namespace:
    """Parses command-line arguments for downloading papers from arXiv.

    Example usage:
        python main.py --query_list "quantum computing" "machine learning" --markdown True --page_size 50 --delay_seconds 5 --num_retries 3 --max_results 20 --sort_by last_updated_date --output_dir ./downloads

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    # Create an ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="A script to download papers from arXiv based on search queries."
    )
    
    # Add an argument for the list of search queries
    parser.add_argument(
        "--query_list", 
        nargs='+',  # Change type=list to nargs='+' to accept multiple arguments
        required=True,  # This argument is mandatory
        help="List of search queries to use for fetching papers. Example: --query_list 'quantum computing' 'machine learning'"
    )

    # Add an argument for converting PDFs to Markdown
    parser.add_argument(
        "--markdown",
        type=bool,
        default=False,
        help="Convert downloaded PDFs to Markdown format. Default is False."
    )
    
    # Add an argument for the number of results to fetch per page
    parser.add_argument(
        "--page_size", 
        type=int,  # Expecting an integer input
        default=100,  # Default value is 100
        help="Number of results to fetch per page. Default is 100. Example: --page_size 50"
    )
    
    # Add an argument for the delay between requests
    parser.add_argument(
        "--delay_seconds", 
        type=int,  # Expecting an integer input
        default=10,  # Default value is 10 seconds
        help="Delay in seconds between requests to avoid hitting the server too quickly. Default is 10. Example: --delay_seconds 5"
    )
    
    # Add an argument for the number of retries on failure
    parser.add_argument(
        "--num_retries", 
        type=int,  # Expecting an integer input
        default=5,  # Default value is 5 retries
        help="Number of times to retry a request in case of failure. Default is 5. Example: --num_retries 3"
    )
    
    # Add an argument for the maximum number of results to return for each query
    parser.add_argument(
        "--max_results", 
        type=int,  # Expecting an integer input
        default=10,  # Default value is 10 results
        help="Maximum number of results to return for each query. Default is 10. Example: --max_results 20"
    )
    
    # Add an argument for sorting the results
    parser.add_argument(
        "--sort_by", 
        type=str,  # Expecting a string input
        choices=["relevance", "last_updated_date", "submitted_date"],  # Valid options for sorting
        default="relevance",  # Default sorting is by relevance
        help="Sort results by specified criteria. Default is 'relevance'. Example: --sort_by last_updated_date"
    )
    
    # Add an argument for the output directory where papers will be saved
    parser.add_argument(
        "--output_dir", 
        type=str,  # Expecting a string input
        default="documents",  # Default output directory is 'documents'
        help="Directory where downloaded papers will be saved. Default is 'documents'. Example: --output_dir ./downloads"
    )
    
    # Parse the arguments and return them as a Namespace object
    return parser.parse_args()

def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Convert a PDF file to markdown text format.
    
    Args:
        pdf_path (str): Path to the PDF file to convert
        
    Returns:
        str: Markdown formatted text extracted from the PDF
        
    Raises:
        FileNotFoundError: If the PDF file does not exist
        pypdf.errors.PdfReadError: If there are issues reading the PDF
    """
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Create PDF reader object using pypdf
            pdf_reader = pypdf.PdfReader(pdf_file)
            
            # Initialize markdown text
            markdown_text = ""
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                # Add page number as header
                markdown_text += f"\n## Page {page_num + 1}\n\n"
                
                # Add page text as paragraphs
                paragraphs = text.split('\n\n')
                for paragraph in paragraphs:
                    # Clean up paragraph text
                    clean_paragraph = paragraph.replace('\n', ' ').strip()
                    if clean_paragraph:
                        markdown_text += f"{clean_paragraph}\n\n"
            
            return markdown_text
            
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        raise
    except pypdf.errors.PdfReadError as e:
        print(f"Error reading PDF file: {str(e)}")
        raise

def main() -> None:
    """
    Main function to execute the arXiv paper downloader.

    This function parses command-line arguments, initializes the arxiv.Client,
    and processes each query to download papers from arXiv.

    Example usage:
        python main.py --query_list "quantum computing" "machine learning" --page_size 50 --delay_seconds 5 --num_retries 3 --max_results 10 --sort_by "relevance" --output_dir "./downloads"

    Command-line arguments:
        --query_list: List of search queries to execute.
        --page_size: Number of results to fetch per page (default: 100).
        --delay_seconds: Delay in seconds between requests (default: 10).
        --num_retries: Number of retries on failure (default: 5).
        --max_results: Maximum number of results to return for each query (default: 10).
        --sort_by: Criteria for sorting results (default: "relevance").
        --output_dir: Directory where downloaded papers will be saved (default: "documents").
    """
    # Parse command-line arguments using the parse_args function
    args = parse_args()

    # Create an instance of the arxiv.Client with specified parameters
    # page_size: number of results per page
    # delay_seconds: delay between requests to avoid overwhelming the server
    # num_retries: number of times to retry a request in case of failure
    client = arxiv.Client(page_size=args.page_size,
                          delay_seconds=args.delay_seconds,
                          num_retries=args.num_retries)
    
    # Check the value of the 'sort_by' argument provided by the user
    # This determines how the search results will be sorted
    if args.sort_by == "relevance":
        # If the user specified "relevance", set the sort criterion to Relevance
        sort_by = arxiv.SortCriterion.Relevance
    elif args.sort_by == "last_updated_date":
        # If the user specified "last_updated_date", set the sort criterion to LastUpdatedDate
        sort_by = arxiv.SortCriterion.LastUpdatedDate
    elif args.sort_by == "submitted_date":
        # If the user specified "submitted_date", set the sort criterion to SubmittedDate
        sort_by = arxiv.SortCriterion.SubmittedDate

    # Iterate over each query provided in the command-line arguments
    for each_query in args.query_list:
        # Create a search object for the current query with specified parameters
        search = arxiv.Search(
            query=each_query,  # The search query string
            max_results=args.max_results,  # Maximum number of results to return
            sort_by=sort_by,  # Sorting criteria for the results
        )

        # Log the current search query being processed
        info(f"Searching for {each_query}")

        # Define the output directory for saving downloaded papers
        # Replace spaces in the query with underscores for the directory name
        output_pdf_dir: str = f"./pdfs/{each_query.replace(' ', '_')}/"
        output_md_dir: str = f"./mds/{each_query.replace(' ', '_')}/"
        
        # Create the output directory if it does not exist
        os.makedirs(output_pdf_dir, exist_ok=True)
        os.makedirs(output_md_dir, exist_ok=True)

        # Iterate over the results returned by the client for the current search
        for index, each_result in enumerate(client.results(search)):
            # Log the progress of downloading results
            info(f"Downloading {index + 1}/{args.max_results}: {each_result.title}")

            try:
                # Attempt to download the PDF of the current result to the output directory
                each_result.download_pdf(dirpath=output_pdf_dir,
                                         filename=f'{each_result.title}.pdf')
                # Log a success message upon successful download
                success(f"Downloaded {each_result.title}")

                try:
                    if args.markdown:
                        # Convert the downloaded PDF to Markdown
                        markdown_text = convert_pdf_to_markdown(f"{output_pdf_dir}{each_result.title}.pdf")
                        
                        # Save the Markdown text to a file
                        with open(f"{output_md_dir}{each_result.title}.md", "w") as markdown_file:
                            markdown_file.write(markdown_text)
                        
                        # Log a success message upon successful conversion
                        success(f"Converted {each_result.title} to Markdown")
                
                except Exception as e:
                    # Log an error message if the conversion fails
                    error(f"Error converting {each_result.title} to Markdown: {e}")

            except Exception as e:
                # Log an error message if the download fails
                error(f"Error downloading {each_result.title}: {e}")
                pass  # Continue to the next result even if an error occurs

# This block checks if the script is being run as the main program.
# The __name__ variable is set to "__main__" when the script is executed directly,
# allowing us to differentiate between running the script and importing it as a module.
if __name__ == "__main__":
    # Call the main function to execute the program logic.
    # This function is expected to handle command-line arguments,
    # perform searches, and manage the downloading of papers.
    main()