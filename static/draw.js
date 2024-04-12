$(() => {
    const width = $('#canvas-wrapper').width();
    const height = width / 16 * 9;

    const rect_to_array = r => [r.x, r.y, r.w, r.h];
    const is_between = (qx, qy, sx, sy, ex, ey) => sx <= qx && qx <= ex && sy <= qy && qy <= ey; 
    const scale_bounds = b => ({x: b.x * width, y: b.y * height, w: b.w * width, h: b.h * height});

    outerBounds = scale_bounds(outerBoundsNormalized);
    innerBounds = scale_bounds(innerBoundsNormalized);

    const canvas = $('#canvas')[0];
    const ctx = canvas.getContext('2d');
    canvas.width = width;
    canvas.height = height;

    const image = new Image();
    image.src = '/static/' + imageFilename; 
    image.onload = () => ctx.drawImage(image, 0, 0, width, height);
    
    let guess = {};
    let dragging = false;
    let submitted = false;

    $('#canvas').on('mousedown', function(e) {
        if (submitted) return;
        guess.x = e.pageX - $(this).offset().left;
        guess.y = e.pageY - $(this).offset().top;
        dragging = true;
    });

    $('#canvas').on('mousemove', function(e) {
        if (submitted) return;
        if (!dragging) return;
        ctx.clearRect(0, 0, width, height);
        ctx.drawImage(image, 0, 0, width, height);
        guess.h = e.pageY - $(this).offset().top - guess.y;
        guess.w = guess.h / 9 * 16;
        ctx.strokeRect(...rect_to_array(guess));
    });

    $('#canvas').on('mouseup', () => {
        if (submitted) return;
        $('#submit-button').prop('disabled', false);
        dragging = false;
    });

    $('#submit-button').click(function() {
        submitted = true;

        $(this).prop('hidden', true);
        $('#instructions').prop('hidden', true);
        $('#next-button').prop('hidden', false);
        $('#feedback').prop('hidden', false);

        const [g, o, i] = [guess, outerBounds, innerBounds];
        if (is_between(g.x, g.y, o.x, o.y, i.x, i.y) && is_between(g.x + g.w, g.y + g.h, i.x + i.w, i.y + i.h, o.x + o.w, o.y + o.h)) {
            $('#correctness').text('Correct!');
            $('#correctness').addClass('text-success');
        } else {
            $('#correctness').text('Incorrect!');
            $('#correctness').addClass('text-danger');
        }
        
        ctx.fillStyle = 'rgba(0, 255, 0, 0.25)';
        ctx.beginPath();
        ctx.rect(...rect_to_array(outerBounds));
        ctx.rect(...rect_to_array(innerBounds));
        ctx.closePath();
        ctx.clip('evenodd');
        ctx.fill();
    });
})
