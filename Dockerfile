# Template Dockerfile: do not modify directly!
# Modified dynamically by moirai.py

FROM debian:latest AS base

RUN apt-get -y update

RUN apt-get -y install \
    git \
    wget \
    bash \
    software-properties-common \
    gnupg2

RUN bash -c "$(wget -O - https://apt.llvm.org/llvm.sh)"

RUN apt-get -y install \
    libllvm13 \
    llvm-13 \
    llvm-13-dev \
    clang-13

RUN git clone https://github.com/llvm/llvm-project.git /llvm-project

WORKDIR /llvm-project

FROM base AS generator

RUN mkdir /output
RUN llvm-tblgen-13 --gen-instr-docs /llvm-project/llvm/lib/Target/ARM/ARM.td -I=/llvm-project/llvm/include > /output/ARM.rst -I/llvm-project/llvm/lib/Target/ARM
RUN llvm-tblgen-13 --gen-instr-docs /llvm-project/llvm/lib/Target/X86/X86.td -I=/llvm-project/llvm/include > /output/X86.rst -I/llvm-project/llvm/lib/Target/X86
RUN llvm-tblgen-13 --gen-instr-docs /llvm-project/llvm/lib/Target/Mips/Mips.td -I=/llvm-project/llvm/include > /output/Mips.rst -I/llvm-project/llvm/lib/Target/Mips
RUN llvm-tblgen-13 --gen-instr-docs /llvm-project/llvm/lib/Target/AArch64/AArch64.td -I=/llvm-project/llvm/include > /output/AArch64.rst -I/llvm-project/llvm/lib/Target/AArch64