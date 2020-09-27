set(sources
    src/tmp.cpp
)

set(exe_sources
		src/main.cpp
		${sources}
)

set(headers
    include/{{ cookiecutter.project_slug }}/tmp.hpp
)
