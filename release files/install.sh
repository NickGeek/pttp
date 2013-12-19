#Installer for PTTP
rm -rf ~/.pttp 2> /dev/null
mkdir ~/.pttp
cp * ~/.pttp/

#Create bash shortcut (requires root)
if which gksudo >/dev/null; then
	gksudo cp pttp /usr/local/bin/
else
	sudo cp pttp /usr/local/bin/
fi
zenity --info --title="PTTP" --text='PTTP has been installed. You can run it by typing "pttp" into your terminal.'
pttp