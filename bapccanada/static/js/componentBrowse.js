import {doAjaxPost} from "./AjaxUtility.js";
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
    return {
        oData: oData,
        sUrl: sUrl
    };
};

$(document).ready(function () {
    $(".addComponentButton").each((index, button) => {
        button.onclick = function () {
            const oParam = fnCreateAddAjaxParameters(this, "add");
            doAjaxPost(oParam.oData, oParam.sUrl);
        }.bind(button)
    });
    const oMetadata = prepareMetadataForAgent(filter_metadata, range_metadata);
    const oManager = new FilterAgent(oMetadata);
});