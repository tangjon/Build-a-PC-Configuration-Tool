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
        }
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
    });

    $('.edit_review').click(function () {
        const review = $(this).parents('.review-card');
        console.log(review)
        review.find('.review-text-body').hide();
        review.find('.review-text-edit').show();
        review.find('.save_review').show();
        $(this).hide()

    });

    $('.save_review').click(function () {
        const review = $(this).parents('.review-card');
        console.log(review)
        review.find('.review-text-edit').hide();
        review.find('.review-text-body').show();
        review.find('.edit_review').show();
        $(this).hide()
    })


});