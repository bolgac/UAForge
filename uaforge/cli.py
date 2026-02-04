import argparse
import sys
from . import generate_user_agent, generate_multiple, update_versions, init_database, __version__
from .core.user_agent import UserAgentGenerator

def main():
    parser = argparse.ArgumentParser(
        description="UAForge - UserAgent Generator CLI\n\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --count 5 --browser Chrome
  %(prog)s --count 10 --output useragents.txt
  %(prog)s --update all
  %(prog)s --init
        """
    )
    
    parser.add_argument("--count", "-c", type=int, default=1, 
                       help="Number of user agents to be created (default: 1)")
    
    parser.add_argument("--browser", "-b", 
                       choices=["Chrome", "Firefox", "Opera", "random"], 
                       default="random", 
                       help="Browser type (default: random)")
    
    parser.add_argument("--output", "-o", 
                       help="Output file (optional)")
    
    parser.add_argument("--update", "-u", 
                       choices=["all", "chrome", "firefox", "opera", "android", "windows", "linux", "mac"],
                       help="Update version information.")
    
    parser.add_argument("--init", action="store_true",
                       help="Populate the database with initial data.")
    
    parser.add_argument("--version", "-v", action="store_true",
                       help="Show version information")
    
    args = parser.parse_args()
    
    if args.version:
        print(f"UAForge v{__version__}")
        return
    
    if args.init:
        print("Initializing the database...")
        if init_database():
            print("Database successfully started!")
        else:
            print("Database initialization failed!")
        return
    
    if args.update:
        if args.update not in "all":
            print(f"{args.update} versions are being updated...")
        try:
            update_versions(args.update)
            print("Update complete!")
        except Exception as e:
            print(f"Error: {e}")
        return
    
    if args.browser == "random":
        import random
        browser = random.choice(["Chrome", "Firefox", "Opera"])
    else:
        browser = args.browser
    
    try:
        generator = UserAgentGenerator()
        
        if args.count == 1:
            user_agent = generator.create_useragent(browser)
            print(user_agent)
            
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(user_agent + "\n")
        else:
            user_agents = generator.get_list(args.count)
            
            for i, ua in enumerate(user_agents, 1):
                print(f"{i:3}. {ua}")
            
            if args.output:
                import os
                from .utils import save_useragents_to_file
                
                if os.path.exists(args.output):
                    overwrite = input(f"The {args.output} file already exists. Should it be overwritten? (yes/no) : ")
                    if overwrite.lower() != 'y' and overwrite.lower() != 'yes':
                        print("The transaction has been cancelled.")
                        return
                
                save_useragents_to_file(user_agents, args.output)
                print(f"\n{args.count} user agent saved to file '{args.output}'.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nTip: Run the '--init' or '--update all' command for the first use.")
        sys.exit(1)

if __name__ == "__main__":
    main()