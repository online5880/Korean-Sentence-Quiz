$(document).ready(function() {
    $('#nickname-form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/text-analysis/',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.status === 'success') {
                    console.log("Redirecting to:", data.redirect);
                    window.location.href = data.redirect;
                } else {
                    alert('닉네임 설정에 실패했습니다. 다시 시도해주세요.');
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error);
                alert('오류가 발생했습니다. 다시 시도해주세요.');
            }
        });
    });
});