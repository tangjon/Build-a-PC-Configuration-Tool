import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';

$(document).ready(function () {
    const csrftoken = getCookie('csrftoken');


    /*
    * REVIEWS
    * - update
    * - delete
    * */
    const fnDeleteReviewParam = function (oElement, sAction) {
        const sUrl = 'delete/';
        const oData = {
            "action": sAction,
            'csrfmiddlewaretoken': csrftoken,
            "pk": oElement.id
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
        const sUrl = 'update/';
        const oData = {
            "action": kwargs['action'],
            "csrfmiddlewaretoken": csrftoken,
            "data": kwargs['data'],
            "pk": kwargs['pk']
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
                "pk": $review[0].id,
                "data": $review.find('.review-text-edit')[0].value
            });
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.success, oParam.error);
        }
    })


    /*
    * BUILDS
    * - edit
    * - delete
    * */

    const fnEditBuildParam = function (kwargs) {
        const sUrl = 'edit/';
        const oData = {
            "action": kwargs['action'],
            "csrfmiddlewaretoken": csrftoken,
            "build_pk": kwargs['build_pk'],
        };
        const fnSuccess = function (e) {
            window.location = e['redirect_url']
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

    $('#edit_build').click(() => {
        const $selected_build = $('.list-group-item.active');
        if ($selected_build.length) {
            // this is bad!
            const build_pk = $selected_build[0].id;
            const oParam = fnEditBuildParam({
                'action': 'edit',
                'build_pk': build_pk,
            });
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.success, oParam.error);
        }
    });


});