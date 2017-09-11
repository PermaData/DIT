from invoke import task


@task
def unit(ctx, debug=False):
    options = ['-vv', '--ignore=systemtests', '--ignore=dit_flow/dit_widget/tests/test_widgets.py']
    if debug:
        options += ['--pdb']

    options = ' '.join(options)
    ctx.run('python -m pytest {options}'.format(options=options), pty=True)


@task
def integration(ctx, debug=False):
    options = ['-vv', 'systemtests']
    if debug:
        options += ['--pdb']

    options = ' '.join(options)
    ctx.run('python -m pytest {options}'.format(options=options), pty=True)


@task
def lint(ctx):
    ctx.run('flake8 .')


@task(lint, default=True)
def all(ctx):
    unit(ctx)
