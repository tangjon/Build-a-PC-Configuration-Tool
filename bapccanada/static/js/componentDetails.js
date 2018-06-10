import doAjaxPost from "./AjaxUtility.js"
import getCookie from "./CookieUtility.js";
import {SAVE_REVIEW_URL} from "./LinkConstants.js";

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

            const fnSuccess = function (data, textStatus) {
                if (data.redirect && data.was_added) {
                    // data.redirect contains the string URL to redirect to
                    window.location.href = data.redirect;
                }
            };

            doAjaxPost(oData, SAVE_REVIEW_URL, fnSuccess)
        }.bind(oSaveButton));
    }
};


$(document).ready(function () {
    fnSetupAddReview();
});