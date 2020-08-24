echo "I am deploying"

cd ~/git/tokyocovid/material-sense/build
aws s3 cp index.html s3://tokyocovid.foostack.org/
aws s3 cp precache-manifest.*.js s3://tokyocovid.foostack.org/
aws s3 cp static s3://tokyocovid.foostack.org/material-sense/static --recursive

echo "I am done"
