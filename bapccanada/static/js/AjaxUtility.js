export function doAjaxPost(oData, sUrl, fnSuccess, fnError) {
    $.ajax({
        type: "POST",
        url: sUrl,
        data: oData,
        dataType: "json",
        success: (fnSuccess && typeof fnSuccess === "function") ? fnSuccess : function (data, textStatus) {
            if (data.redirect) {
                // data.redirect contains the string URL to redirect to
                window.location.href = data.redirect;
            }
        },
        error: (fnError && typeof fnError === "function") ? fnError : function (error) {
            console.log("Error! " + error);
        }
    });
}

export function doAjaxGet(oData, sUrl, fnSuccess, fnError) {
    $.ajax({
        type: "GET",
        url: sUrl,
        data: oData,
        dataType: "json",
        success: (fnSuccess && typeof fnSuccess === "function") ? fnSuccess : function (data, textStatus) {
            if (data.redirect) {
                // data.redirect contains the string URL to redirect to
                window.location.href = data.redirect;
            }
        },
        error: (fnError && typeof fnError === "function") ? fnError : function (error) {
            console.log("Error! " + error);
        }
    });
}