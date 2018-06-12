import doAjaxPost from "./AjaxUtility.js";
import {COMPONENT_CHANGE} from "./LinkConstants.js";
import getCookie from "./CookieUtility.js";
import FilterAgent from "./FilterAgent.js"
import prepareMetadataForAgent from "./FilterAgentUtils.js";

const csrftoken = getCookie('csrftoken');
const fnCreateAddAjaxParameters = function (oElement, sAction) {
    const sUrl = COMPONENT_CHANGE;
    const oData = {
        "slug": oElement.id,
        "action": sAction,
        'csrfmiddlewaretoken': csrftoken
    };
    const fnSuccess = function (data, textStatus) {
        if (data.redirect) {
            // data.redirect contains the string URL to redirect to
            window.location.href = data.redirect;
        }
    };

    return {
        oData: oData,
        sUrl: sUrl,
        fnSuccess: fnSuccess
    };
};

$(document).ready(function () {
    $(".addComponentButton").each((index, button) => {
        button.onclick = function () {
            const oParam = fnCreateAddAjaxParameters(this, "add");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.fnSuccess);
        }.bind(button)
    });
    const oMetadata = prepareMetadataForAgent(filter_metadata);
    const oManager = new FilterAgent(oMetadata);
});