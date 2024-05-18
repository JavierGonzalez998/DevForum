reflex init
reflex export --frontend-only --loglevel debug
rm - rf public
unzip frontend.zip -d public
rm -f frontend.zip
