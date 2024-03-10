import sys
from server import app
from monitorizareFisiere import monitor_folder

def main():
    if len(sys.argv) < 2:
        print("Utilizare: python main.py [server/monitorizare]")
        sys.exit()

    mod = sys.argv[1]

    if mod == 'server':
        print("Pornește serverul Flask...")
        app.run(debug=True)
    elif mod == 'monitorizare':
        print("Pornește monitorizarea folderului de intrari")
        monitor_folder()
    else:
        print("Opțiune necunoscută. Utilizare: python main.py [server/monitorizare]")

if __name__ == '__main__':
    main()