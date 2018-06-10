import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';

$(document).ready(function () {
    const csrftoken = getCookie('csrftoken');
    const fnDeleteReviewParam = function (oElement, sAction) {
        const sUrl = oElement.id + '/delete';
        const oData = {
            "action": sAction,
            'csrfmiddlewaretoken': csrftoken
        };
        const fnSuccess = function (e) {

            $(oElement).remove();
            location.reload()
        };

        const fnError = function (e) {
            console.log(e);
        };
        return {
            oData: oData,
            sUrl: sUrl,
            success: fnSuccess,
            error: fnError
        };
    };

    const fnUpdateReviewParam = function (oElement, kwargs) {
        const sUrl = kwargs['id'] + '/update';
        const oData = {
            "action": kwargs['action'],
            "csrfmiddlewaretoken": csrftoken,
            "data": kwargs['data']
        };
        const fnSuccess = function (e) {
            oElement.find('.review-text-edit').hide();
            oElement.find('.save_review').hide()
            oElement.find('.edit_review').show();
            oElement.find('.review-text-body')[0].innerText = e.data.content
            oElement.find('.review-text-body').show();
        };

        const fnError = function (e) {
            console.log(e);
        };
        return {
            oData: oData,
            sUrl: sUrl,
            success: fnSuccess,
            error: fnError
        };
    };

    $('.delete_review').click(function () {
        const $review = $(this).parents('.review-card');
        const review = $review[0];
        const review_component = $review.find('.review-component')[0];
        const message_confirm = `Are you sure you want to delete review ${review.id} : ${review_component.innerText}?`;
        if (window.confirm(message_confirm)) {
            const oParam = fnDeleteReviewParam(review, "delete");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.success, oParam.error);
        }
    });

    $('.edit_review').click(function () {
        const $review = $(this).parents('.review-card');
        $review.find('.review-text-body').hide();
        $review.find('.review-text-edit').show();
        $review.find('.save_review').show();
        $(this).hide()
    });

    $('.save_review').click(function () {
        const $review = $(this).parents('.review-card');
        const message_confirm = `Are you sure you want to save review`;
        if (window.confirm(message_confirm)) {
            const oParam = fnUpdateReviewParam($review, {
                "action": "update",
                "id": $review[0].id,
                "data": $review.find('.review-text-edit')[0].value
            });
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.success, oParam.error);
        }

    })


});