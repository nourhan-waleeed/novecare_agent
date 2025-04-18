/** @odoo-module **/
import { registry } from "@web/core/registry";

let recordID = false;
registry.category("services").add("Chat Dashboard", {
    dependencies: ["action"],
    start(env) {
        env.bus.addEventListener("ACTION_MANAGER:UI-UPDATED", () => {
            console.log('------------------')
            const modalDialog = document.querySelector('.modal-dialog');
            if (!modalDialog) {


    let currentUrl = window.location.href;

    var chatDashboard = currentUrl.includes('model=chat.dashboard&view_type=form');
    if (chatDashboard) {
        const hashParams = window.location.hash.substring(1);

        const params = Object.fromEntries(
            hashParams.split('&').map(param => param.split('='))
        );
        var recordId = params.id;
        console.log('Extracted chatDashboard Record ID:', recordId);
        recordID =recordId;
            }
            }
        });
        }
});


function getChat(id){

    console.log('clicked idddddddd',id);
    console.log('recordd idddddddd',recordID);
             const env = owl.Component.env;
                 const result =  env.services.rpc('/web/dataset/call_kw/chat.dashboard/get_chat', {
                                                 model: 'chat.dashboard',
                                                 method: 'get_chat',
                                                 args: [id,recordID],
                                                kwargs: {}
                                                }).then(result => {
                                                console.log('result', result);

                                                env.services.action.doAction({
                                                    type: 'ir.actions.client',
                                                    tag: 'reload',
                                                });
                                                });
}
window.getChat = getChat;
