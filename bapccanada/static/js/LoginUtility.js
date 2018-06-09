import {LOGIN_URL, NEXT_URL_PARAMETER_PREFIX} from "./LinkConstants.js";

/**
 *  Checks to see if user is authenticated, front-end edition
 *  Relies on base.html's user_authenticated variable
 *
 * @param fnOkCallback        if user is authenticated, perform this action
 * @param sNextDirect         if user is not authenticated, add a parameter to allow them to return somewhere
 */
export default function fnCheckUserAuthentication(fnOkCallback, sNextDirect) {
    if (!user_authenticated) {
        let sRedirectUrl = LOGIN_URL;
        if (sNextDirect) {
            sRedirectUrl += NEXT_URL_PARAMETER_PREFIX + sNextDirect;
        }

        window.location.href = sRedirectUrl;
    } else {
        fnOkCallback();
    }
}