# Use the official Fedora image as a starting point
FROM fedora:latest

# Install sudo and the tools needed for mock
# Also create the 'mock' group
RUN dnf -y update && \
    dnf -y install sudo git mock mock-core-configs rpm-build rpmdevtools && \
    dnf clean all

# Create a non-root user named 'vscode' and add it to the 'mock' group
# This user will have passwordless sudo access
RUN useradd --uid 1000 --user-group --create-home vscode && \
    usermod -aG mock,wheel vscode && \
    echo '%wheel ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/wheel

USER vscode
WORKDIR /home/vscode
RUN rpmdev-setuptree
