# CLI web_build for Ren'Py 7.6.3 (stock launcher is GUI-only for web).
# Copied into the SDK's launcher/game/ by the build script before building.

init python:

    def web_build_command():
        ap = renpy.arguments.ArgumentParser(description="Build a web distribution.")
        ap.add_argument("web_project", help="The path to the project directory.")
        ap.add_argument("--destination", "--dest", default=None, action="store",
                        help="Copy result to this directory after build.")
        args = ap.parse_args()

        if WEB_PATH is None:
            raise SystemExit(
                "Web support is not available. Extract renpy-*-web.zip into the SDK 'web' folder."
            )

        p = project.Project(args.web_project)
        project.current = p

        build_web(p, gui=False)

        built = get_web_destination(p)
        print("Built web game at:", built)

        if args.destination:
            dest = os.path.abspath(args.destination)
            src = os.path.abspath(built)
            if src != dest:
                if os.path.exists(dest):
                    shutil.rmtree(dest)
                shutil.copytree(src, dest)
                print("Copied to:", dest)

        return False

    renpy.arguments.register_command("web_build", web_build_command)
