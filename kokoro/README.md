# kokoro build

This directory contains all the logic for building Secure Shell releases in the
kokoro continuous integration platform.
It runs inside of the docker container (see [/Dockerfile]).
This allows us to be isolated from the kokoro runtime and be nice & stable.
