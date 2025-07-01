FROM scratch

ADD ./dockerImage/MSCCD.tar ./

WORKDIR /works

CMD [ "/bin/bash" ]