FROM python@sha256:2407c61b1a18067393fecd8a22cf6fceede893b6aaca817bf9fbfe65e33614a3
# 3.10.13-slim-bookworm

ENV APPDIR="/App"
WORKDIR ${APPDIR}

RUN apt-get update &&  \
    apt-get install --no-install-recommends -y git && \
    apt-get clean -y && \
    apt-get autoclean -y && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY ./ $APPDIR/
RUN pip install --no-cache-dir -r $APPDIR/requirements.txt

# Entrypoint
RUN chmod a+x $APPDIR/run.py
ENTRYPOINT ["python","/App/run.py"]
