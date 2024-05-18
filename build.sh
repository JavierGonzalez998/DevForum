reflex export --loglevel debug
rm - rf public/frontend
unzip frontend.zip -d public/frontend
rm -f frontend.zip
reflex run