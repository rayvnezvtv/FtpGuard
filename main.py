from ftplib import FTP

ftp = FTP()
ftp.connect("127.0.0.1", 25)
ftp.login("rayan", "Respons11!")
print("Connecté :", ftp.getwelcome())
ftp.quit()