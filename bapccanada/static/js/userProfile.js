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
        const fnSuccess = function (e) {
            $(this).remove();
            console.log(e.statusText, "success");

        };

        const fnError = function (e) {
            console.log(e, "error");
            console.log(e.statusText)

        };
        return {
            oData: oData,
            sUrl: sUrl,
            success: fnSuccess,
            error: fnError
        };
    };

    $('.delete_review').click(function () {
        const review = $(this).parents('.review-card')[0];
        if (window.confirm(`Are you sure you want to delete review ${review.id}?`)) {
            const oParam = fnDeleteReviewParam(review, "delete");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.success, oParam.error);
        }
    });

    $('.edit_review').click(function () {
        const review = $(this).parents('.review-card');
        review.find('.review-text-body').hide();
        review.find('.review-text-edit').show();
        review.find('.save_review').show();
        $(this).hide()
    });

    $('.save_review').click(function () {
        const review = $(this).parents('.review-card');
        review.find('.review-text-edit').hide();
        review.find('.review-text-body').show();
        review.find('.edit_review').show();
        $(this).hide()
    })


});