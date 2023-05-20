FROM archlinux
WORKDIR /home
COPY . .
RUN dir
RUN pacman -Syyu hugo git --noconfirm
RUN hugo
