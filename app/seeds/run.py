import typer
from app.seeds.service import run_all, run_categories, run_posts, run_tags, run_users

app = typer.Typer(help="Seeds CLI")


@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los seeds creados")


@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")


@app.command("categories")
def categories():
    run_categories()
    typer.echo("Categorías cargadas")


@app.command("tags")
def tags():
    run_tags()
    typer.echo("Tags cargados")


@app.command("posts")
def posts():
    run_posts()
    typer.echo("Posts cargados")


if __name__ == "__main__":
    app()
