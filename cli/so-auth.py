import sys

import click
import requests
from config import Config, file
from requests.exceptions import ConnectionError, Timeout


SERVER_BAD_JSON_STRING = 'server returned an incorrectly formatted response'
CREATE_USER_SHORT_DESC = 'Creates a new user for Security Onion'
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def print_separator():
    click.echo('...')


class AppState(object):
    def __init__(self, verbose, debug, config_filename):
        self.verbose = verbose
        self.debug = debug
        # noinspection PyBroadException
        try:
            f = file(config_filename)
            config = Config(f)

            # Begin reading in values from config file
            config_readline = 'API_URI'
            try:
                self.api_uri = config.API_URI
                config_readline = 'DEBUG'
                self.debug = config.DEBUG
            except Exception as e:
                if self.debug:
                    click.echo(e)
                click.echo(f'Failed to read key {config_readline} from config file')
                sys.exit(-1)
        except Exception as e:
            click.echo(f'Could not read config file "{config_filename}"')
            click.echo()
            click.echo(e)
            sys.exit(-1)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('-v', '--verbose', is_flag=True)
@click.option('-d', '--debug', is_flag=True)
@click.option('-c', '--config', default='so-auth.cfg', help='Sets alternative config filename')
def cli(ctx, verbose, debug, config):
    ctx.obj = AppState(verbose, debug, config)


@cli.command('create_user', short_help=CREATE_USER_SHORT_DESC, context_settings=CONTEXT_SETTINGS)
@click.argument('username')
@click.password_option(help='Password to assign new user (must be at least 6 characters)')
@click.pass_obj
def create_user(appstate, username, password):
    """
        Create new user USERNAME
    """
    try:
        if appstate.verbose:
            click.echo(f'Making post request to {appstate.api_uri} with username: {username}')

        response = requests.post(appstate.api_uri, json=dict(
            username=username,
            password=password
        ))

        print_separator()

        try:
            response_json = response.json()
            if appstate.verbose:
                click.echo(f'Received following response from server: {response_json}')
                if response:
                    sys.exit(0)
                else:
                    sys.exit(-1)
            if response:
                click.echo(
                    response_json.get('message', f'Successfully created user {username} but {SERVER_BAD_JSON_STRING}')
                )
                sys.exit(0)
            else:
                click.echo(
                    response_json.get('message', f'Could not create user {username} and {SERVER_BAD_JSON_STRING}')
                )
                sys.exit(-1)

        except ValueError as e:
            if appstate.debug:
                click.echo(e)
            if appstate.verbose:
                click.echo('Response does not contain JSON')
            else:
                click.echo('Unexpected API response, please check service logs')
            sys.exit(-1)
        except Exception as e:
            if appstate.debug:
                click.echo(e)
            click.echo('Unhandled error occurred')
            sys.exit(-1)

    except ConnectionError as e:
        if appstate.debug:
            click.echo(e)
        else:
            click.echo('Connection to api server could not be established')
        sys.exit(-1)

    except Timeout as e:
        if appstate.debug:
            click.echo(e)
        else:
            click.echo('Connection to api server timed out')
        sys.exit(-1)

    except Exception as e:
        if appstate.debug:
            click.echo(e)
        else:
            click.echo('Unhandled exception occurred while making request to api server')
        sys.exit(-1)


if __name__ == '__main__':
    cli()

