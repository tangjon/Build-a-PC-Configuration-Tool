import {doAjaxPost} from "./AjaxUtility.js"
import getCookie from "./CookieUtility.js";
import {COMPONENT_CHANGE, SAVE_REVIEW_URL} from "./LinkConstants.js";

const csrftoken = getCookie('csrftoken');

const fnSetupAddReview = function () {
    if (user_authenticated) {
        let iRating = 0;
        const oStarControl = $("#star-input-control");
        oStarControl.barrating({
            theme: "fontawesome-stars",
            onSelect: (value, text, event) => {
                if (value) {
                    iRating = parseInt(value);
                } else {
                    iRating = 0;
                }
            }
        });

        const oSaveButton = $(".add-review-save");
        const oReviewContent = $(".add-review-text-area");

        oSaveButton.on('click', function () {
            const oData = {
                "slug": this[0].id,
                "action": "new",
                "rating": iRating,
                "content": oReviewContent.val(),
                'csrfmiddlewaretoken': csrftoken
            };

            doAjaxPost(oData, SAVE_REVIEW_URL)
        }.bind(oSaveButton));
    }
};

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

let bIsFilterRequest = false;
if (window.location.href.indexOf("filters") !== -1) {
    bIsFilterRequest = true;
    const sStrippedUrl = window.location.href.split("?filters=")[0];
    window.history.pushState('Browse Components', 'Browse Components', sStrippedUrl);
}


$(document).ready(function () {


    $(".detailAddButton").each((index, button) => {
        button.onclick = function () {
            console.log(this);
            const oParam = fnCreateAddAjaxParameters(this, "add");
            doAjaxPost(oParam.oData, oParam.sUrl);
        }.bind(button)
    });
    fnSetupAddReview();
});