from string import Template


def _load_template(name: str):
    with open(f"templates/{name}.template.html", "r") as f:
        return Template(f.read())


_page = _load_template("page")
_power = _load_template("power")


def page(body: str):
    return _page.substitute(body=body)


def power(on: bool):
    return _power.substitute(
        on_disabled="disabled" if on else "",
        off_disabled="disabled" if not on else "",
    )
