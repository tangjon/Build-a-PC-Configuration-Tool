import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';

$(document).ready(function () {
    const csrftoken = getCookie('csrftoken');
    const fnDeleteReviewParam = function (oElement, sAction) {
        const sUrl = oElement.id + '/delete';
        const oData = {
            "slug": oElement.id,
            "action": sAction,
            'csrfmiddlewaretoken': csrftoken
        };
        const fnSuccess = function () {
            location.reload()
        };
        return {
            oData: oData,
            sUrl: sUrl,
            fnSuccess: fnSuccess
        };
    };

    $('.delete_review').click(function () {

        if (window.confirm(`Are you sure you want to delete review ${this.id}?`)) {
            const oParam = fnDeleteReviewParam(this, "delete");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.fnSuccess);
            $(this).closest('.review-card').remove();
        }

    })


})