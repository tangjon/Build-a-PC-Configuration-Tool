import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';
import fnCheckUserAuthentication from './LoginUtility.js';
import {BUILD_SAVE, COMPONENT_CHANGE, BUILD_URL} from './LinkConstants.js';

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

const fnAlertHandler = function (sAlertId, sMsg) {
    const oAlert = $("#" + sAlertId);
    oAlert.text(sMsg);
    oAlert.addClass("visible");
    setTimeout(() => {
        oAlert.removeClass("visible")
    }, 2500);
};

const fnSetupSaveModal = function () {
    const oNameInput = $(".build-name");
    const oSaveAsButton = $(".save-as-button");
    const oSaveBuildButton = $(".save-modal-confirm");
    const oSaveModal = $(".save-as-modal");
    const oSaveForm = $(".save-modal-form");
    const fnHandleReject = function (sErrorMsg) {
        fnAlertHandler("errorAlert", sErrorMsg);
    };
    const fnHandleSuccess = function (sSuccessMsg) {
        fnAlertHandler("successAlert", sSuccessMsg);
    };

    oSaveAsButton.on('click', function () {
       fnCheckUserAuthentication(() => {
           oSaveModal.modal('show');
       }, BUILD_URL);
    });

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
                oSavePromise.resolve("Build " + data.saved_name + " saved!");
            } else {
                oSavePromise.reject(data.error + "!");
            }
        };
        const fnError = function (error) {
            oSavePromise.reject("Request failed: " + error);
        };

        doAjaxPost(oData, BUILD_SAVE, fnSuccess, fnError);

        oSavePromise.then((sSuccessMessage) => {
            fnHandleSuccess(sSuccessMessage);
        }, (sErrorMessage) => {
            fnHandleReject(sErrorMessage);
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
