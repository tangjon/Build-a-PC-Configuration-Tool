$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    $(".addComponentButton").each((index, button) => {
        button.onclick = function () {
            $.ajax({
                type: "POST",
                url: '/build/add/',
                data: {
                    "slug": this.id,
                    "action": "add",
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: "json",
                success: function (data, textStatus) {
                    if (data.redirect) {
                        // data.redirect contains the string URL to redirect to
                        window.location.href = data.redirect;
                    }
                }
            });
        }.bind(button)
    });

    $(".removeComponentButton").each((index, button) => {
        button.onclick = function () {
            $.ajax({
                type: "POST",
                url: '/build/add/',
                data: {
                    "slug": this.id,
                    "action": "remove",
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: "json",
                success: function (data, textStatus) {
                    if (data.redirect) {
                        // data.redirect contains the string URL to redirect to
                        window.location.href = data.redirect;
                    }
                }
            });
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
            error: function(error) {
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
