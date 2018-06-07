import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';
import {BUILD_SAVE, COMPONENT_CHANGE} from './LinkConstants.js';

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

const fnSetupSaveModal = function () {
    const oNameInput = $(".build-name");
    const oSaveBuildButton = $(".save-modal-confirm");
    const oSaveModal = $(".save-as-modal");
    const oSaveForm = $(".save-modal-form");

    oSaveForm.bind("keypress", function (event) {
        const iKeycode = (event.keyCode ? event.keyCode : event.which);
        if (iKeycode === 13) {
            // trigger form submit instead of just closing modal
            event.preventDefault();
            oSaveBuildButton.click();
        }
    });

    oSaveBuildButton.on('click', function () {
        const oSavePromise = $.Deferred();
        const oData = {
            "build_name": oNameInput.val(),
            "action": "save",
            'csrfmiddlewaretoken': csrftoken
        };
        const fnSuccess = function (data, textStatus) {
            if (data.was_added) {
                oSavePromise.resolve("Build saved!")
            } else {
                oSavePromise.reject("Server error: " + data.error);
            }
        };
        const fnError = function (error) {
            oSavePromise.reject("Build saving failed!");
        };

        doAjaxPost(oData, BUILD_SAVE, fnSuccess, fnError);

        oSavePromise.then((resolvedMsg) => {
            console.log(resolvedMsg);

        }, (rejectedMsg) => {
            console.log(rejectedMsg);
        });

        oNameInput.val('');
        oSaveModal.modal('hide');
    }.bind(oSaveBuildButton))
};

$(document).ready(function () {
    $(".addComponentButton").each((index, button) => {
        button.onclick = function () {
            const oParam = fnCreateAddAjaxParameters(this, "add");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.fnSuccess);
        }.bind(button)
    });

    $(".removeComponentButton").each((index, button) => {
        button.onclick = function () {
            const oParam = fnCreateAddAjaxParameters(this, "remove");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.fnSuccess);
        }.bind(button)
    });

    fnSetupSaveModal();
});
