"""**Know Your UniBorg**
◇ list of all loaded plugins
◆ `.helpme`\n
◇ to know Data Center
◆ `.dc`\n
◇ powered by
◆ `.config`\n
◇ to know syntax
◆ `.syntax` <plugin name>
"""
import logging
import sys
import time
from telethon import events, functions, __version__


@borg.on(utils.admin_cmd(pattern="helpme ?(.*)", allow_sudo=True))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    splugin_name = event.pattern_match.group(1)
    if splugin_name in borg._plugins:
        s_help_string = borg._plugins[splugin_name].__doc__
    else:
        s_help_string = ""
    _, check_sgnirts = check_data_base_heal_th()

    current_run_time = utils.time_formatter((time.time() - BOT_START_TIME))
    total, used, free = shutil.disk_usage("/")
    total = utils.humanbytes(total)
    used = utils.humanbytes(used)
    free = utils.humanbytes(free)

    help_string = "@UniBorg\n"
    help_string += f"✅ <b>UpTime</b> <code>{current_run_time}</code>\n"
    help_string += f"✅ <b>Python</b> <code>{sys.version}</code>\n"
    help_string += f"✅ <b>Telethon</b> <code>{__version__}</code>\n"
    help_string += f"{check_sgnirts} <b>Database</b>\n"
    help_string += f"<b>Total Disk Space</b>: <code>{total}</code>\n"
    help_string += f"<b>Used Disk Space</b>: <code>{used}</code>\n"
    help_string += f"<b>Free Disk Space</b>: <code>{free}</code>\n\n"
    help_string += f"UserBot Forked from https://github.com/udf/uniborg"
    borg._iiqsixfourstore[str(event.chat_id)] = {}
    borg._iiqsixfourstore[
        str(event.chat_id)
    ][
        str(event.id)
    ] = help_string + "\n\n" + s_help_string
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER  # pylint:disable=E0602
    if tgbotusername is not None:
        results = await borg.inline_query(
            tgbotusername,
            help_string + "\n\n" + s_help_string
        )
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
    else:
        await event.reply(
            help_string + "\n\n" + s_help_string,
            parse_mode="html"
        )

    await event.delete()


@borg.on(utils.admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())


@borg.on(utils.admin_cmd(pattern="config"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(functions.help.GetConfigRequest())  # pylint:disable=E0602
    result = result.stringify()
    logger.info(result)
    await event.edit("""Telethon UserBot powered by @UniBorg""")


@borg.on(utils.admin_cmd(pattern="syntax (.*)"))
async def _(event):
    if event.fwd_from:
        return
    plugin_name = event.pattern_match.group(1)
    if plugin_name in borg._plugins:
        help_string = borg._plugins[plugin_name].__doc__
        unload_string = f"Use `.unload {plugin_name}` to remove this plugin.\n           © @UniBorg"
        if help_string:
            plugin_syntax = f"Syntax for plugin **{plugin_name}**:\n\n{help_string}\n{unload_string}"
        else:
            plugin_syntax = f"No DOCSTRING has been setup for {plugin_name} plugin."
    else:
        plugin_syntax = "Enter valid **Plugin** name.\nDo `.exec ls stdplugins` or `.helpme` to get list of valid plugin names."
    await event.edit(plugin_syntax)
