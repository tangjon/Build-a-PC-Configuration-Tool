import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';
import COMPONENT_CHANGE from './LinkConstants.js';

$(document).ready(function () {
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

    const oSaveBuildButton = $(".save-modal-confirm");

    oSaveBuildButton.on('click', function () {
        const oSavePromise = $.Deferred();

        $.ajax({
            type: "POST",
            url: '/build/save/',
            data: {
                "build_name": $(".build-name").val(),
                "action": "save",
                'csrfmiddlewaretoken': csrftoken
            },
            dataType: "json",
            success: function (data, textStatus) {
                if (data.was_added) {
                    // data.redirect contains the string URL to redirect to
                    oSavePromise.resolve("Build saved!")
                } else {
                    oSavePromise.reject("Server error: " + data.error);
                }
            },
            error: function (error) {
                oSavePromise.reject("Build saving failed!");
            }
        });

        oSavePromise.then((resolvedMsg) => {
            console.log(resolvedMsg);

        }, (rejectedMsg) => {
            console.log(rejectedMsg);
        });

        $(".build-name").val('');
        $(".save-as-modal").modal('hide');
    }.bind(oSaveBuildButton))
});
