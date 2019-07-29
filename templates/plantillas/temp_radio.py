{%for form in dbform%}
    <fieldset data-role="controlgroup" data-type="horizontal">
        <legend>{{form[1]}}:</legend>
        <input type="radio" name="{{form[0]}}" id="{{form[0]}}a" value="c"  checked="checked">
        <label for="{{form[0]}}a">C</label>
        <input type="radio" name="{{form[0]}}" id="{{form[0]}}b" value="na">
        <label for="{{form[0]}}b">NA</label>
    </fieldset> 
{%endfor%}
