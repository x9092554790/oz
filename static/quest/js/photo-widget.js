/**
 * Created by Adm on 01.08.2016.
 */
$(document).ready(function() {
    var imgs_url = "/quest/google_doc_get_random_player_images";
    var imgs_url2 = "https://googledrive.com/host/";
    var update_count = 1;
    var cur_imgs = {};
    var cur_imgs_coords = [];
    var cur_imgs_coords_idx = [];
    var canvas = document.getElementById("imgs_canvas");
    var canvas_container = document.getElementById("imgs_container");
    var width = canvas.width;
    var height = canvas.height;
    var ctx = canvas.getContext("2d");
    var max_rows = 3;
    var max_colummns = 8;
    var dh = height/max_rows;
    var dw = width/max_colummns;
    var dh_min = dh*0.7;
    var dh_max = dh*1.9;
    var dw_min = dw*0.7;
    var dw_max = dw*1.9;
    var draw_interval = 100;
    var drawed_idx = [];
    var draw_h_min = 50;
    var draw_w_min = 50;
    var draw_border = 2;
    var imaged_idx = [];
    var redraw_iter = 20;
    var redraw_interval = 50;
    var get_images_interval = 1000;

    var hidden, visibilityState, visibilityChange;

    if (typeof document.hidden !== "undefined")
        hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
    else if (typeof document.msHidden !== "undefined")
        hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";

    var document_hidden = document[hidden];

    document.addEventListener(visibilityChange, function()
    {
        if(document_hidden != document[hidden])
            document_hidden = document[hidden];
    });


    function getImages()
    {
        if(!document_hidden)
            $.get(imgs_url, {'count': update_count})
                .done(function(data)
                {
                    if(data && 'items' in data)
                        updateImgs(data['items'],
                            function()
                            {
                                setTimeout(getImages, get_images_interval);
                            });
                })
                .fail(function()
                {
                    setTimeout(getImages, get_images_interval);
                });
        else
            setTimeout(getImages, get_images_interval);
    }

    function updateImgs(imgs, done)
    {
        for(var i = 0; i < imgs.length; i++)
        {
            var idx = getActualIdx();
            cur_imgs[idx] = imgs[i];
            drawImg(idx, done);
        }
    }

    function getActualIdx()
    {
        var act_idx = [];

        for(var i = 0; i < cur_imgs_coords_idx.length; i++)
        {
            var cell = cur_imgs_coords[cur_imgs_coords_idx[i]];
            var act_width = $(document).width();
            var act_height = canvas_container.clientHeight;
            if(cell[0] < act_width && cell[1] < act_height)
                if(imaged_idx.indexOf(cur_imgs_coords_idx[i]) == -1)
                    return cur_imgs_coords_idx[i];
                else
                    act_idx.push(cur_imgs_coords_idx[i]);
        }

        return act_idx[getRandomInt(0, act_idx.length-1)];
    }

    function shuffle(array)
    {
       var copy = [], n = array.length, i;
          while (n)
          {
            i = Math.floor(Math.random() * array.length);
            if (i in array) {
              copy.push(array[i]);
              delete array[i];
              n--;
            }
          }

      return copy;
    }

    function getRandomInt(min, max)
    {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function drawImg(idx, done)
    {
        var url = imgs_url2 + cur_imgs[idx];
        var img = new Image();
        img.setAttribute('data-idx', idx);
        img.onload = function()
        {
            var img = $(this)[0];
            var idx = parseInt($(this).attr('data-idx'));
            var cell = cur_imgs_coords[idx];
            redrawImage(cell, img, done);
            imaged_idx.push(idx);
        };
        img.onerror = function()
        {
            var img = $(this)[0];
            var idx = parseInt($(this).attr('data-idx'));
            var cell = cur_imgs_coords[idx];
            imaged_idx.push(idx);
            if(done)
                done();
        };
        img.src = url;
    }

    function redrawImage(cell, img, done)
    {
        var cur_iter = 0;
        var interval_id = setInterval(function()
        {
            drawImageProp(ctx, img, cell[0]+draw_border, cell[1]+draw_border, cell[2]-2*draw_border, cell[3]-2*draw_border,0.5,0.4);
            if(cur_iter < redraw_iter) {
                var a = 1.0 * (redraw_iter - cur_iter) / redraw_iter;
                ctx.fillStyle = "rgba(255,255,255," + a + ")";
                ctx.fillRect(cell[0], cell[1], cell[2], cell[3]);
                cur_iter += 1;
            }
            else {
                clearInterval(interval_id);
                if(done)
                    done();
            }
        }, redraw_interval);
    }

    function drawImageProp(ctx, img, x, y, w, h, offsetX, offsetY)
    {
        if (arguments.length === 2) {
            x = y = 0;
            w = ctx.canvas.width;
            h = ctx.canvas.height;
        }

        // default offset is center
        offsetX = typeof offsetX === "number" ? offsetX : 0.5;
        offsetY = typeof offsetY === "number" ? offsetY : 0.5;

        // keep bounds [0.0, 1.0]
        if (offsetX < 0) offsetX = 0;
        if (offsetY < 0) offsetY = 0;
        if (offsetX > 1) offsetX = 1;
        if (offsetY > 1) offsetY = 1;

        var iw = img.width,
            ih = img.height,
            r = Math.min(w / iw, h / ih),
            nw = iw * r,   // new prop. width
            nh = ih * r,   // new prop. height
            cx, cy, cw, ch, ar = 1;

        // decide which gap to fill
        if (nw < w) ar = w / nw;
        if (Math.abs(ar - 1) < 1e-14 && nh < h) ar = h / nh;  // updated
        nw *= ar;
        nh *= ar;

        // calc source rectangle
        cw = iw / (nw / w);
        ch = ih / (nh / h);

        cx = (iw - cw) * offsetX;
        cy = (ih - ch) * offsetY;

        // make sure source rectangle is valid
        if (cx < 0) cx = 0;
        if (cy < 0) cy = 0;
        if (cw > iw) cw = iw;
        if (ch > ih) ch = ih;

        // fill image in dest. rectangle
        ctx.drawImage(img, cx, cy, cw, ch,  x, y, w, h);
    }

    function initImgsGrid()
    {
        var cur_h = 0; var cur_w = 0;
        var hh = 0;
        var ww = 0;
        var row_sidx = 0;
        var row_eidx = -1;
        var row_cols = 0;
        var is_end = false;

        while(true)
        {
            row_cols = 0;
            while(true)
            {
                ww = getRandomInt(dw_min, dw_max);
                hh = getRandomInt(dh_min, dh_max);
                var dww = ww;

                for(var i = row_sidx; i <= row_eidx; i++)
                {
                    var cell = cur_imgs_coords[i];
                    if(cell[0] <= cur_w && cell[0] + cell[2] > cur_w)
                    {
                        cur_h = cell[1] + cell[3];
                        if(cur_w + ww > cell[0] + cell[2])
                            dww = cell[0] + cell[2] - cur_w;
                        break;
                    }
                }

                for(var i = row_sidx; i <= row_eidx; i++)
                {
                    var cell = cur_imgs_coords[i];
                    if(cell[0] > cur_w && cell[1] + cell[3] > cur_h && cur_w + ww > cell[0])
                    {
                        ww = cell[0] - cur_w;
                        break;
                    }
                }

                for(var i = row_eidx+1; i <= row_eidx+row_cols; i++)
                {
                    var cell = cur_imgs_coords[i];
                    if(cell[0] + cell[2] > cur_w)
                    {
                        hh = cell[1]-cur_h;
                        break;
                    }
                }

                if(cur_w + ww > width)
                    ww = width - cur_w;
                if(cur_h + hh > height)
                    hh = height - cur_h;

                cur_imgs_coords.push([cur_w, cur_h, ww, hh]);
                if(ww >= draw_w_min && hh >= draw_h_min)
                    cur_imgs_coords_idx.push(cur_imgs_coords.length-1);
                row_cols += 1;

                cur_w += (dww < ww ? dww : ww);

                if(cur_w >= width) //next line
                {
                    var is_end = true;
                    row_sidx = row_eidx + 1;
                    row_eidx += row_cols;
                    cur_w = 0;
                    for(var i = row_sidx + 1; i <= row_eidx; i++)
                    {
                        var cell = cur_imgs_coords[i];
                        if(cell[1] + cell[3] < height) {
                            is_end = false;
                            break;
                        }
                    }
                    if(is_end) {
                        cur_imgs_coords_idx = shuffle(cur_imgs_coords_idx);
                        return;
                    }
                    break;
                }
            }
        }
    }

    function drawCells(done)
    {
        while(true)
        {
            var cur_draw_idx = 0;
            var ridx = getRandomInt(0, cur_imgs_coords.length - 1);
            var finded = false;
            for (var i = ridx; i < cur_imgs_coords.length; i++)
                if (drawed_idx.indexOf(i) == -1)
                { cur_draw_idx = i;
                    finded = true;
                    break;
                }
            if (!finded)
                for (var i = ridx; i >= 0; i--)
                    if (drawed_idx.indexOf(i) == -1)
                    {
                        cur_draw_idx = i;
                        break;
                    }

            var cell = cur_imgs_coords[cur_draw_idx];
            if(cell[2] > 0 && cell[3] > 0) //cur_imgs_coords_idx.indexOf(cur_draw_idx) != -1)
                drawCell(cell[0], cell[1], cell[2], cell[3]);
            drawed_idx.push(cur_draw_idx);
            if (drawed_idx.length >= cur_imgs_coords.length) {
                done();
                return;
            }

            if(cell[2] > 0 && cell[3] > 0) //cur_imgs_coords_idx.indexOf(cur_draw_idx) != -1)
                break;
        }

        setTimeout(function(){drawCells(done)}, draw_interval);
    }

    function drawCell(x, y, w, h)
    {
        var r = getRandomInt(0,255);
        var g = getRandomInt(0,255);
        var b = getRandomInt(0,255);
        var a = 0.2;
        ctx.fillStyle = "rgba("+r+","+g+","+b+","+a+")";
        ctx.fillRect(x,y,w,h);
    }

    initImgsGrid();
    drawCells(getImages);
});