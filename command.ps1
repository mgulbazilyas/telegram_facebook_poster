curl \
https://bbuseruploads.s3.amazonaws.com/fd96ed93-2b32-46a7-9d2b-ecbc0988516a/downloads/396e7977-71fd-4592-8723-495ca4cfa7cc/phantomjs-2.1.1-linux-x86_64.tar.bz2?Signature=jTUCUyls7s7tQA06RkcuO9RtycY%3D&Expires=1623685541&AWSAccessKeyId=AKIA6KOSE3BNJRRFUUX6&versionId=null&response-content-disposition=attachment%3B%20filename%3D%22phantomjs-2.1.1-linux-x86_64.tar.bz2%22
-o phantomjs.tar.bz2

Set-Variable -Name "server" -Value "65.21.171.220"
scp *.py lian@${server}:~/telegram_facebook_poster/
scp *.py root@137.220.57.157:/root/telegram_facebook_poster/

scp config.py gukly@gukly.com:/home2/gukly/telegram_facebook_poster
sudo {http,https,ftp}_proxy=http://mMvnM5:q58u1L@195.85.194.198:8000/ python telegram_handle.py


ssh gukly@gukly.com


source /home2/gukly/virtualenv/coffee_subscriptions_backend/3.7/bin/activate  && cd telegram_facebook_poster

export HTTP_PROXY="http://mMvnM5:q58u1L@195.85.194.198:8000"
export HTTPS_PROXY="https://mMvnM5:q58u1L@195.85.194.198:8000"