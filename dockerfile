FROM python@sha256:2407c61b1a18067393fecd8a22cf6fceede893b6aaca817bf9fbfe65e33614a3
# 3.10.13-slim-bookworm

ENV APPDIR="/App"
WORKDIR ${APPDIR}

ARG CAR_CHECK_API
ENV CAR_CHECK_API=${CAR_CHECK_API}

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/linux64/chrome-headless-shell-linux64.zip && \
    apt-get update && \
    unzip chrome-headless-shell-linux64.zip && \
    mv chrome-headless-shell-linux64/chrome-headless-shell /usr/local/bin/google-chrome && \
    chmod +x /usr/local/bin/google-chrome && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/130.0.6723.116/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    rm chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -r chromedriver-linux64

# Install Python dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r $APPDIR/requirements.txt

# Set environment variables
ENV DISPLAY=:99
# ENV PATH="/usr/local/bin:$PATH"

# Application code
COPY ./ $APPDIR/

RUN chmod a+x $APPDIR/run.py
ENTRYPOINT ["python","/App/run.py"]
