__all__ = ['mapgen']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['rgbToHsv', 'tallRows', 'DIR_RIGHT', 'genRandom', 'tileSize', 'setDirFromEnum', 'drawTiles', 'LEFT', 'randomElement', 'rows', 'getEnumFromDir', 'reset', 'cells', 'hslToRgb', 'DIR_UP', 'rgbToHsl', 'getTiles', 'DOWN', 'hsvToRgb', 'narrowCols', 'mapgen', 'rgbString', 'Map', 'DIR_LEFT', 'getRandomInt', 'UP', 'drawCells', 'cols', 'shuffle', 'DIR_DOWN', 'randomColor', 'RIGHT'])
@Js
def PyJsHoisted_rgbToHsl_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['s', 'h', 'max', 'b', 'min', 'd', 'r', 'g', 'l'])
    PyJsComma(PyJsComma(var.put('r', Js(255.0), '/'),var.put('g', Js(255.0), '/')),var.put('b', Js(255.0), '/'))
    var.put('max', var.get('Math').callprop('max', var.get('r'), var.get('g'), var.get('b')))
    var.put('min', var.get('Math').callprop('min', var.get('r'), var.get('g'), var.get('b')))
    var.put('l', ((var.get('max')+var.get('min'))/Js(2.0)))
    if (var.get('max')==var.get('min')):
        var.put('h', var.put('s', Js(0.0)))
    else:
        var.put('d', (var.get('max')-var.get('min')))
        var.put('s', ((var.get('d')/((Js(2.0)-var.get('max'))-var.get('min'))) if (var.get('l')>Js(0.5)) else (var.get('d')/(var.get('max')+var.get('min')))))
        while 1:
            SWITCHED = False
            CONDITION = (var.get('max'))
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('r')):
                SWITCHED = True
                var.put('h', (((var.get('g')-var.get('b'))/var.get('d'))+(Js(6.0) if (var.get('g')<var.get('b')) else Js(0.0))))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('g')):
                SWITCHED = True
                var.put('h', (((var.get('b')-var.get('r'))/var.get('d'))+Js(2.0)))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('b')):
                SWITCHED = True
                var.put('h', (((var.get('r')-var.get('g'))/var.get('d'))+Js(4.0)))
                break
            SWITCHED = True
            break
        var.put('h', Js(6.0), '/')
    return Js([var.get('h'), var.get('s'), var.get('l')])
PyJsHoisted_rgbToHsl_.func_name = 'rgbToHsl'
var.put('rgbToHsl', PyJsHoisted_rgbToHsl_)
@Js
def PyJsHoisted_hslToRgb_(h, s, l, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'l':l, 'this':this, 'arguments':arguments}, var)
    var.registers(['l', 's', 'hue2rgb', 'h', 'b', 'g', 'r', 'q', 'p'])
    @Js
    def PyJsHoisted_hue2rgb_(p, q, t, this, arguments, var=var):
        var = Scope({'p':p, 'q':q, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['q', 'p', 't'])
        if (var.get('t')<Js(0.0)):
            var.put('t', Js(1.0), '+')
        if (var.get('t')>Js(1.0)):
            var.put('t', Js(1.0), '-')
        if (var.get('t')<(Js(1.0)/Js(6.0))):
            return (var.get('p')+(((var.get('q')-var.get('p'))*Js(6.0))*var.get('t')))
        if (var.get('t')<(Js(1.0)/Js(2.0))):
            return var.get('q')
        if (var.get('t')<(Js(2.0)/Js(3.0))):
            return (var.get('p')+(((var.get('q')-var.get('p'))*((Js(2.0)/Js(3.0))-var.get('t')))*Js(6.0)))
        return var.get('p')
    PyJsHoisted_hue2rgb_.func_name = 'hue2rgb'
    var.put('hue2rgb', PyJsHoisted_hue2rgb_)
    pass
    if (var.get('s')==Js(0.0)):
        var.put('r', var.put('g', var.put('b', var.get('l'))))
    else:
        pass
        var.put('q', ((var.get('l')*(Js(1.0)+var.get('s'))) if (var.get('l')<Js(0.5)) else ((var.get('l')+var.get('s'))-(var.get('l')*var.get('s')))))
        var.put('p', ((Js(2.0)*var.get('l'))-var.get('q')))
        var.put('r', var.get('hue2rgb')(var.get('p'), var.get('q'), (var.get('h')+(Js(1.0)/Js(3.0)))))
        var.put('g', var.get('hue2rgb')(var.get('p'), var.get('q'), var.get('h')))
        var.put('b', var.get('hue2rgb')(var.get('p'), var.get('q'), (var.get('h')-(Js(1.0)/Js(3.0)))))
    var.put('r', Js(255.0), '*')
    var.put('g', Js(255.0), '*')
    var.put('b', Js(255.0), '*')
    return Js([var.get('r'), var.get('g'), var.get('b')])
PyJsHoisted_hslToRgb_.func_name = 'hslToRgb'
var.put('hslToRgb', PyJsHoisted_hslToRgb_)
@Js
def PyJsHoisted_rgbToHsv_(r, g, b, this, arguments, var=var):
    var = Scope({'r':r, 'g':g, 'b':b, 'this':this, 'arguments':arguments}, var)
    var.registers(['s', 'h', 'max', 'b', 'min', 'v', 'd', 'r', 'g'])
    PyJsComma(PyJsComma(var.put('r', (var.get('r')/Js(255.0))),var.put('g', (var.get('g')/Js(255.0)))),var.put('b', (var.get('b')/Js(255.0))))
    var.put('max', var.get('Math').callprop('max', var.get('r'), var.get('g'), var.get('b')))
    var.put('min', var.get('Math').callprop('min', var.get('r'), var.get('g'), var.get('b')))
    var.put('v', var.get('max'))
    var.put('d', (var.get('max')-var.get('min')))
    var.put('s', (Js(0.0) if (var.get('max')==Js(0.0)) else (var.get('d')/var.get('max'))))
    if (var.get('max')==var.get('min')):
        var.put('h', Js(0.0))
    else:
        while 1:
            SWITCHED = False
            CONDITION = (var.get('max'))
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('r')):
                SWITCHED = True
                var.put('h', (((var.get('g')-var.get('b'))/var.get('d'))+(Js(6.0) if (var.get('g')<var.get('b')) else Js(0.0))))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('g')):
                SWITCHED = True
                var.put('h', (((var.get('b')-var.get('r'))/var.get('d'))+Js(2.0)))
                break
            if SWITCHED or PyJsStrictEq(CONDITION, var.get('b')):
                SWITCHED = True
                var.put('h', (((var.get('r')-var.get('g'))/var.get('d'))+Js(4.0)))
                break
            SWITCHED = True
            break
        var.put('h', Js(6.0), '/')
    return Js([var.get('h'), var.get('s'), var.get('v')])
PyJsHoisted_rgbToHsv_.func_name = 'rgbToHsv'
var.put('rgbToHsv', PyJsHoisted_rgbToHsv_)
@Js
def PyJsHoisted_hsvToRgb_(h, s, v, this, arguments, var=var):
    var = Scope({'h':h, 's':s, 'v':v, 'this':this, 'arguments':arguments}, var)
    var.registers(['s', 'h', 'b', 'p', 'f', 'g', 'r', 't', 'v', 'q', 'i'])
    pass
    var.put('i', var.get('Math').callprop('floor', (var.get('h')*Js(6.0))))
    var.put('f', ((var.get('h')*Js(6.0))-var.get('i')))
    var.put('p', (var.get('v')*(Js(1.0)-var.get('s'))))
    var.put('q', (var.get('v')*(Js(1.0)-(var.get('f')*var.get('s')))))
    var.put('t', (var.get('v')*(Js(1.0)-((Js(1.0)-var.get('f'))*var.get('s')))))
    while 1:
        SWITCHED = False
        CONDITION = ((var.get('i')%Js(6.0)))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(0.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('v')),var.put('g', var.get('t'))),var.put('b', var.get('p')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('q')),var.put('g', var.get('v'))),var.put('b', var.get('p')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('p')),var.put('g', var.get('v'))),var.put('b', var.get('t')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('p')),var.put('g', var.get('q'))),var.put('b', var.get('v')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('t')),var.put('g', var.get('p'))),var.put('b', var.get('v')))
            break
        if SWITCHED or PyJsStrictEq(CONDITION, Js(5.0)):
            SWITCHED = True
            PyJsComma(PyJsComma(var.put('r', var.get('v')),var.put('g', var.get('p'))),var.put('b', var.get('q')))
            break
        SWITCHED = True
        break
    var.put('r', Js(255.0), '*')
    var.put('g', Js(255.0), '*')
    var.put('b', Js(255.0), '*')
    return Js([var.get('r'), var.get('g'), var.get('b')])
PyJsHoisted_hsvToRgb_.func_name = 'hsvToRgb'
var.put('hsvToRgb', PyJsHoisted_hsvToRgb_)
@Js
def PyJsHoisted_rgbString_(rgb, this, arguments, var=var):
    var = Scope({'rgb':rgb, 'this':this, 'arguments':arguments}, var)
    var.registers(['rgb', 'b', 'g', 'r'])
    var.put('r', var.get('Math').callprop('floor', var.get('rgb').get('0')))
    var.put('g', var.get('Math').callprop('floor', var.get('rgb').get('1')))
    var.put('b', var.get('Math').callprop('floor', var.get('rgb').get('2')))
    return ((((((Js('rgb(')+var.get('r'))+Js(','))+var.get('g'))+Js(','))+var.get('b'))+Js(')'))
PyJsHoisted_rgbString_.func_name = 'rgbString'
var.put('rgbString', PyJsHoisted_rgbString_)
pass
pass
pass
pass
pass
var.put('DIR_UP', Js(0.0))
var.put('DIR_RIGHT', Js(1.0))
var.put('DIR_DOWN', Js(2.0))
var.put('DIR_LEFT', Js(3.0))
@Js
def PyJs_anonymous_0_(dir, this, arguments, var=var):
    var = Scope({'dir':dir, 'this':this, 'arguments':arguments}, var)
    var.registers(['dir'])
    if (var.get('dir').get('x')==(-Js(1.0))):
        return var.get('DIR_LEFT')
    if (var.get('dir').get('x')==Js(1.0)):
        return var.get('DIR_RIGHT')
    if (var.get('dir').get('y')==(-Js(1.0))):
        return var.get('DIR_UP')
    if (var.get('dir').get('y')==Js(1.0)):
        return var.get('DIR_DOWN')
PyJs_anonymous_0_._set_name('anonymous')
var.put('getEnumFromDir', PyJs_anonymous_0_)
@Js
def PyJs_anonymous_1_(dir, dirEnum, this, arguments, var=var):
    var = Scope({'dir':dir, 'dirEnum':dirEnum, 'this':this, 'arguments':arguments}, var)
    var.registers(['dir', 'dirEnum'])
    if (var.get('dirEnum')==var.get('DIR_UP')):
        var.get('dir').put('x', Js(0.0))
        var.get('dir').put('y', (-Js(1.0)))
    else:
        if (var.get('dirEnum')==var.get('DIR_RIGHT')):
            var.get('dir').put('x', Js(1.0))
            var.get('dir').put('y', Js(0.0))
        else:
            if (var.get('dirEnum')==var.get('DIR_DOWN')):
                var.get('dir').put('x', Js(0.0))
                var.get('dir').put('y', Js(1.0))
            else:
                if (var.get('dirEnum')==var.get('DIR_LEFT')):
                    var.get('dir').put('x', (-Js(1.0)))
                    var.get('dir').put('y', Js(0.0))
PyJs_anonymous_1_._set_name('anonymous')
var.put('setDirFromEnum', PyJs_anonymous_1_)
var.put('tileSize', Js(8.0))
@Js
def PyJs_anonymous_2_(numCols, numRows, tiles, this, arguments, var=var):
    var = Scope({'numCols':numCols, 'numRows':numRows, 'tiles':tiles, 'this':this, 'arguments':arguments}, var)
    var.registers(['tiles', 'numCols', 'numRows'])
    var.get(u"this").put('numCols', var.get('numCols'))
    var.get(u"this").put('numRows', var.get('numRows'))
    var.get(u"this").put('numTiles', (var.get('numCols')*var.get('numRows')))
    var.get(u"this").put('widthPixels', (var.get('numCols')*var.get('tileSize')))
    var.get(u"this").put('heightPixels', (var.get('numRows')*var.get('tileSize')))
    var.get(u"this").put('tiles', var.get('tiles'))
    var.get(u"this").callprop('resetCurrent')
    var.get(u"this").callprop('parseWalls')
PyJs_anonymous_2_._set_name('anonymous')
var.put('Map', PyJs_anonymous_2_)
@Js
def PyJs_anonymous_3_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get(u"this").put('currentTiles', var.get(u"this").get('tiles').callprop('split', Js('')))
PyJs_anonymous_3_._set_name('anonymous')
var.get('Map').get('prototype').put('resetCurrent', PyJs_anonymous_3_)
@Js
def PyJs_anonymous_4_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['edges', 'toIndex', 'makePath', 'x', 'y', 'that', 'i', 'visited'])
    var.put('that', var.get(u"this"))
    var.get(u"this").put('paths', Js([]))
    var.put('visited', Js({}))
    @Js
    def PyJs_anonymous_5_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'y'])
        if ((((var.get('x')>=(-Js(2.0))) and (var.get('x')<(var.get('that').get('numCols')+Js(2.0)))) and (var.get('y')>=Js(0.0))) and (var.get('y')<var.get('that').get('numRows'))):
            return ((var.get('x')+Js(2.0))+(var.get('y')*(var.get('that').get('numCols')+Js(4.0))))
    PyJs_anonymous_5_._set_name('anonymous')
    var.put('toIndex', PyJs_anonymous_5_)
    var.put('edges', Js({}))
    var.put('i', Js(0.0))
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get(u"this").get('numRows')):
        try:
            #for JS loop
            var.put('x', (-Js(2.0)))
            while (var.get('x')<(var.get(u"this").get('numCols')+Js(2.0))):
                try:
                    def PyJs_LONG_6_(var=var):
                        return (((((var.get(u"this").callprop('getTile', (var.get('x')-Js(1.0)), var.get('y'))!=Js('|')) or (var.get(u"this").callprop('getTile', (var.get('x')+Js(1.0)), var.get('y'))!=Js('|'))) or (var.get(u"this").callprop('getTile', var.get('x'), (var.get('y')-Js(1.0)))!=Js('|'))) or (var.get(u"this").callprop('getTile', var.get('x'), (var.get('y')+Js(1.0)))!=Js('|'))) or (var.get(u"this").callprop('getTile', (var.get('x')-Js(1.0)), (var.get('y')-Js(1.0)))!=Js('|')))
                    if ((var.get(u"this").callprop('getTile', var.get('x'), var.get('y'))==Js('|')) and (((PyJs_LONG_6_() or (var.get(u"this").callprop('getTile', (var.get('x')-Js(1.0)), (var.get('y')+Js(1.0)))!=Js('|'))) or (var.get(u"this").callprop('getTile', (var.get('x')+Js(1.0)), (var.get('y')-Js(1.0)))!=Js('|'))) or (var.get(u"this").callprop('getTile', (var.get('x')+Js(1.0)), (var.get('y')+Js(1.0)))!=Js('|')))):
                        var.get('edges').put(var.get('i'), Js(True))
                finally:
                        PyJsComma((var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1)),(var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1)))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    @Js
    def PyJs_anonymous_7_(tx, ty, this, arguments, var=var):
        var = Scope({'tx':tx, 'ty':ty, 'this':this, 'arguments':arguments}, var)
        var.registers(['ty', 'pad', 'turnAround', 'getStartPoint', 'dirEnum', 'lastPoint', 'init_tx', 'init_ty', 'path', 'dir', 'tx', 'point', 'init_dirEnum', 'turn'])
        var.put('dir', Js({}))
        pass
        if var.get('edges').contains(var.get('toIndex')((var.get('tx')+Js(1.0)), var.get('ty'))):
            var.put('dirEnum', var.get('DIR_RIGHT'))
        else:
            if var.get('edges').contains(var.get('toIndex')(var.get('tx'), (var.get('ty')+Js(1.0)))):
                var.put('dirEnum', var.get('DIR_DOWN'))
            else:
                PyJsTempException = JsToPyException((((Js("tile shouldn't be 1x1 at ")+var.get('tx'))+Js(','))+var.get('ty')))
                raise PyJsTempException
        var.get('setDirFromEnum')(var.get('dir'), var.get('dirEnum'))
        var.put('tx', var.get('dir').get('x'), '+')
        var.put('ty', var.get('dir').get('y'), '+')
        var.put('init_tx', var.get('tx'))
        var.put('init_ty', var.get('ty'))
        var.put('init_dirEnum', var.get('dirEnum'))
        var.put('path', Js([]))
        pass
        pass
        pass
        pass
        @Js
        def PyJs_anonymous_8_(tx, ty, dirEnum, this, arguments, var=var):
            var = Scope({'tx':tx, 'ty':ty, 'dirEnum':dirEnum, 'this':this, 'arguments':arguments}, var)
            var.registers(['ty', 'py', 's', 'a', 'dirEnum', 'px', 'c', 'dir', 'tx'])
            var.put('dir', Js({}))
            var.get('setDirFromEnum')(var.get('dir'), var.get('dirEnum'))
            if var.get('edges').contains(var.get('toIndex')((var.get('tx')+var.get('dir').get('y')), (var.get('ty')-var.get('dir').get('x')))).neg():
                var.put('pad', (Js(5.0) if var.get('that').callprop('isFloorTile', (var.get('tx')+var.get('dir').get('y')), (var.get('ty')-var.get('dir').get('x'))) else Js(0.0)))
            var.put('px', (((-var.get('tileSize'))/Js(2.0))+var.get('pad')))
            var.put('py', (var.get('tileSize')/Js(2.0)))
            var.put('a', ((var.get('dirEnum')*var.get('Math').get('PI'))/Js(2.0)))
            var.put('c', var.get('Math').callprop('cos', var.get('a')))
            var.put('s', var.get('Math').callprop('sin', var.get('a')))
            return Js({'x':(((var.get('px')*var.get('c'))-(var.get('py')*var.get('s')))+((var.get('tx')+Js(0.5))*var.get('tileSize'))),'y':(((var.get('px')*var.get('s'))+(var.get('py')*var.get('c')))+((var.get('ty')+Js(0.5))*var.get('tileSize')))})
        PyJs_anonymous_8_._set_name('anonymous')
        var.put('getStartPoint', PyJs_anonymous_8_)
        while Js(True):
            var.get('visited').put(var.get('toIndex')(var.get('tx'), var.get('ty')), Js(True))
            var.put('point', var.get('getStartPoint')(var.get('tx'), var.get('ty'), var.get('dirEnum')))
            if var.get('turn'):
                var.put('lastPoint', var.get('path').get((var.get('path').get('length')-Js(1.0))))
                if (var.get('dir').get('x')==Js(0.0)):
                    var.get('point').put('cx', var.get('point').get('x'))
                    var.get('point').put('cy', var.get('lastPoint').get('y'))
                else:
                    var.get('point').put('cx', var.get('lastPoint').get('x'))
                    var.get('point').put('cy', var.get('point').get('y'))
            var.put('turn', Js(False))
            var.put('turnAround', Js(False))
            if var.get('edges').contains(var.get('toIndex')((var.get('tx')+var.get('dir').get('y')), (var.get('ty')-var.get('dir').get('x')))):
                var.put('dirEnum', ((var.get('dirEnum')+Js(3.0))%Js(4.0)))
                var.put('turn', Js(True))
            else:
                if var.get('edges').contains(var.get('toIndex')((var.get('tx')+var.get('dir').get('x')), (var.get('ty')+var.get('dir').get('y')))):
                    pass
                else:
                    if var.get('edges').contains(var.get('toIndex')((var.get('tx')-var.get('dir').get('y')), (var.get('ty')+var.get('dir').get('x')))):
                        var.put('dirEnum', ((var.get('dirEnum')+Js(1.0))%Js(4.0)))
                        var.put('turn', Js(True))
                    else:
                        var.put('dirEnum', ((var.get('dirEnum')+Js(2.0))%Js(4.0)))
                        var.put('turnAround', Js(True))
            var.get('setDirFromEnum')(var.get('dir'), var.get('dirEnum'))
            var.get('path').callprop('push', var.get('point'))
            if var.get('turnAround'):
                var.get('path').callprop('push', var.get('getStartPoint')((var.get('tx')-var.get('dir').get('x')), (var.get('ty')-var.get('dir').get('y')), ((var.get('dirEnum')+Js(2.0))%Js(4.0))))
                var.get('path').callprop('push', var.get('getStartPoint')(var.get('tx'), var.get('ty'), var.get('dirEnum')))
            var.put('tx', var.get('dir').get('x'), '+')
            var.put('ty', var.get('dir').get('y'), '+')
            if (((var.get('tx')==var.get('init_tx')) and (var.get('ty')==var.get('init_ty'))) and (var.get('dirEnum')==var.get('init_dirEnum'))):
                var.get('that').get('paths').callprop('push', var.get('path'))
                break
    PyJs_anonymous_7_._set_name('anonymous')
    var.put('makePath', PyJs_anonymous_7_)
    var.put('i', Js(0.0))
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get(u"this").get('numRows')):
        try:
            #for JS loop
            var.put('x', (-Js(2.0)))
            while (var.get('x')<(var.get(u"this").get('numCols')+Js(2.0))):
                try:
                    if (var.get('edges').contains(var.get('i')) and var.get('visited').contains(var.get('i')).neg()):
                        var.get('visited').put(var.get('i'), Js(True))
                        var.get('makePath')(var.get('x'), var.get('y'))
                finally:
                        PyJsComma((var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1)),(var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1)))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
PyJs_anonymous_4_._set_name('anonymous')
var.get('Map').get('prototype').put('parseWalls', PyJs_anonymous_4_)
@Js
def PyJs_anonymous_9_(x, y, this, arguments, var=var):
    var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
    var.registers(['x', 'y'])
    if ((((var.get('x')>=Js(0.0)) and (var.get('x')<var.get(u"this").get('numCols'))) and (var.get('y')>=Js(0.0))) and (var.get('y')<var.get(u"this").get('numRows'))):
        return (var.get('x')+(var.get('y')*var.get(u"this").get('numCols')))
PyJs_anonymous_9_._set_name('anonymous')
var.get('Map').get('prototype').put('posToIndex', PyJs_anonymous_9_)
@Js
def PyJs_anonymous_10_(x, y, this, arguments, var=var):
    var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
    var.registers(['x', 'y'])
    if ((((var.get('x')>=Js(0.0)) and (var.get('x')<var.get(u"this").get('numCols'))) and (var.get('y')>=Js(0.0))) and (var.get('y')<var.get(u"this").get('numRows'))):
        return var.get(u"this").get('currentTiles').get(var.get(u"this").callprop('posToIndex', var.get('x'), var.get('y')))
    def PyJs_LONG_11_(var=var):
        return ((((var.get('x')==(-Js(1.0))) and (var.get(u"this").callprop('getTile', (var.get('x')+Js(1.0)), var.get('y'))==Js('|'))) and (var.get(u"this").callprop('isFloorTile', (var.get('x')+Js(1.0)), (var.get('y')+Js(1.0))) or var.get(u"this").callprop('isFloorTile', (var.get('x')+Js(1.0)), (var.get('y')-Js(1.0))))) or (((var.get('x')==var.get(u"this").get('numCols')) and (var.get(u"this").callprop('getTile', (var.get('x')-Js(1.0)), var.get('y'))==Js('|'))) and (var.get(u"this").callprop('isFloorTile', (var.get('x')-Js(1.0)), (var.get('y')+Js(1.0))) or var.get(u"this").callprop('isFloorTile', (var.get('x')-Js(1.0)), (var.get('y')-Js(1.0))))))
    if PyJs_LONG_11_():
        return Js('|')
    if (((var.get('x')==(-Js(1.0))) and var.get(u"this").callprop('isFloorTile', (var.get('x')+Js(1.0)), var.get('y'))) or ((var.get('x')==var.get(u"this").get('numCols')) and var.get(u"this").callprop('isFloorTile', (var.get('x')-Js(1.0)), var.get('y')))):
        return Js(' ')
PyJs_anonymous_10_._set_name('anonymous')
var.get('Map').get('prototype').put('getTile', PyJs_anonymous_10_)
@Js
def PyJs_anonymous_12_(tile, this, arguments, var=var):
    var = Scope({'tile':tile, 'this':this, 'arguments':arguments}, var)
    var.registers(['tile'])
    return (((var.get('tile')==Js(' ')) or (var.get('tile')==Js('.'))) or (var.get('tile')==Js('o')))
PyJs_anonymous_12_._set_name('anonymous')
var.get('Map').get('prototype').put('isFloorTileChar', PyJs_anonymous_12_)
@Js
def PyJs_anonymous_13_(x, y, this, arguments, var=var):
    var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
    var.registers(['x', 'y'])
    return var.get(u"this").callprop('isFloorTileChar', var.get(u"this").callprop('getTile', var.get('x'), var.get('y')))
PyJs_anonymous_13_._set_name('anonymous')
var.get('Map').get('prototype').put('isFloorTile', PyJs_anonymous_13_)
@Js
def PyJs_anonymous_14_(ctx, left, top, print, this, arguments, var=var):
    var = Scope({'ctx':ctx, 'left':left, 'top':top, 'print':print, 'this':this, 'arguments':arguments}, var)
    var.registers(['j', 'print', 'top', 'tile', 'ctx', 'pelletSize', 'energizerSize', 'x', 't', 'path', 'y', 'i', 'left'])
    var.get('ctx').callprop('save')
    var.get('ctx').callprop('translate', Js(0.5), Js(0.5))
    var.get('ctx').callprop('translate', var.get('left'), var.get('top'))
    var.get('ctx').callprop('beginPath')
    var.get('ctx').callprop('rect', Js(0.0), Js(0.0), var.get(u"this").get('widthPixels'), var.get(u"this").get('heightPixels'))
    var.get('ctx').callprop('clip')
    if var.get('print').neg():
        var.get('ctx').put('fillStyle', Js('#000'))
        var.get('ctx').callprop('fillRect', Js(0.0), Js(0.0), var.get(u"this").get('widthPixels'), var.get(u"this").get('heightPixels'))
    var.get('ctx').put('fillStyle', (Js('#333') if var.get('print') else var.get(u"this").get('wallFillColor')))
    var.get('ctx').put('strokeStyle', (Js('#333') if var.get('print') else var.get(u"this").get('wallStrokeColor')))
    pass
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get(u"this").get('paths').get('length')):
        try:
            var.put('path', var.get(u"this").get('paths').get(var.get('i')))
            var.get('ctx').callprop('beginPath')
            var.get('ctx').callprop('moveTo', var.get('path').get('0').get('x'), var.get('path').get('0').get('y'))
            #for JS loop
            var.put('j', Js(1.0))
            while (var.get('j')<var.get('path').get('length')):
                try:
                    if (var.get('path').get(var.get('j')).get('cx')!=var.get('undefined')):
                        var.get('ctx').callprop('quadraticCurveTo', var.get('path').get(var.get('j')).get('cx'), var.get('path').get(var.get('j')).get('cy'), var.get('path').get(var.get('j')).get('x'), var.get('path').get(var.get('j')).get('y'))
                    else:
                        var.get('ctx').callprop('lineTo', var.get('path').get(var.get('j')).get('x'), var.get('path').get(var.get('j')).get('y'))
                finally:
                        (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
            var.get('ctx').callprop('quadraticCurveTo', var.get('path').get((var.get('j')-Js(1.0))).get('x'), var.get('path').get('0').get('y'), var.get('path').get('0').get('x'), var.get('path').get('0').get('y'))
            var.get('ctx').callprop('fill')
            var.get('ctx').callprop('stroke')
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.put('pelletSize', (var.get('tileSize') if var.get('print') else Js(2.0)))
    var.put('energizerSize', Js(3.0))
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get(u"this").get('numRows')):
        try:
            #for JS loop
            var.put('x', Js(0.0))
            while (var.get('x')<var.get(u"this").get('numCols')):
                try:
                    var.put('t', var.get(u"this").callprop('getTile', var.get('x'), var.get('y')))
                    if (((var.get('t')==Js('o')) or (var.get('t')==Js('.'))) or (var.get('t')==Js(' '))):
                        var.get('ctx').put('fillStyle', (Js('#bbb') if var.get('print') else var.get(u"this").get('pelletColor')))
                        var.get('ctx').callprop('fillRect', (((var.get('x')*var.get('tileSize'))+(var.get('tileSize')/Js(2.0)))-(var.get('pelletSize')/Js(2.0))), (((var.get('y')*var.get('tileSize'))+(var.get('tileSize')/Js(2.0)))-(var.get('pelletSize')/Js(2.0))), var.get('pelletSize'), var.get('pelletSize'))
                finally:
                        (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    var.get('ctx').put('strokeStyle', (Js('rgba(0,0,0,0.3)') if var.get('print') else Js('rgba(255,255,255,0.3)')))
    var.get('ctx').callprop('beginPath')
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<=var.get(u"this").get('numRows')):
        try:
            var.get('ctx').callprop('moveTo', Js(0.0), (var.get('y')*var.get('tileSize')))
            var.get('ctx').callprop('lineTo', var.get(u"this").get('widthPixels'), (var.get('y')*var.get('tileSize')))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('x', Js(0.0))
    while (var.get('x')<=var.get(u"this").get('numCols')):
        try:
            var.get('ctx').callprop('moveTo', (var.get('x')*var.get('tileSize')), Js(0.0))
            var.get('ctx').callprop('lineTo', (var.get('x')*var.get('tileSize')), var.get(u"this").get('heightPixels'))
        finally:
                (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
    var.get('ctx').callprop('stroke')
    if var.get(u"this").get('name'):
        var.get('ctx').put('textBaseline', Js('top'))
        var.get('ctx').put('font', Js('20px sans-serif'))
        var.get('ctx').put('fillStyle', (Js('#000') if var.get('print') else Js('#fff')))
        var.get('ctx').callprop('fillText', var.get(u"this").get('name'), Js(0.0), (var.get('tileSize')/Js(2.0)))
    var.get('ctx').callprop('restore')
PyJs_anonymous_14_._set_name('anonymous')
var.get('Map').get('prototype').put('draw', PyJs_anonymous_14_)
@Js
def PyJs_anonymous_15_(ctx, left, top, this, arguments, var=var):
    var = Scope({'ctx':ctx, 'left':left, 'top':top, 'this':this, 'arguments':arguments}, var)
    var.registers(['j', 'print', 'top', 'tile', 'ctx', 'x', 'y', 'i', 'left'])
    var.put('print', Js(True))
    var.get('ctx').callprop('save')
    var.get('ctx').callprop('translate', Js(0.5), Js(0.5))
    var.get('ctx').callprop('translate', var.get('left'), var.get('top'))
    var.get('ctx').callprop('beginPath')
    var.get('ctx').callprop('rect', Js(0.0), Js(0.0), var.get(u"this").get('widthPixels'), var.get(u"this").get('heightPixels'))
    var.get('ctx').callprop('clip')
    pass
    pass
    pass
    var.get('ctx').put('lineWidth', Js(2.0))
    var.get('ctx').put('strokeStyle', Js('rgba(0,0,0,0.8)'))
    var.get('ctx').callprop('beginPath')
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<(var.get(u"this").get('numRows')-Js(1.0))):
        try:
            #for JS loop
            var.put('x', Js(0.0))
            while (var.get('x')<(var.get(u"this").get('numCols')-Js(1.0))):
                try:
                    if var.get(u"this").callprop('isFloorTile', var.get('x'), var.get('y')):
                        if var.get(u"this").callprop('isFloorTile', (var.get('x')+Js(1.0)), var.get('y')):
                            var.get('ctx').callprop('moveTo', (var.get('x')*var.get('tileSize')), (var.get('y')*var.get('tileSize')))
                            var.get('ctx').callprop('lineTo', ((var.get('x')+Js(1.0))*var.get('tileSize')), (var.get('y')*var.get('tileSize')))
                        if var.get(u"this").callprop('isFloorTile', var.get('x'), (var.get('y')+Js(1.0))):
                            var.get('ctx').callprop('moveTo', (var.get('x')*var.get('tileSize')), (var.get('y')*var.get('tileSize')))
                            var.get('ctx').callprop('lineTo', (var.get('x')*var.get('tileSize')), ((var.get('y')+Js(1.0))*var.get('tileSize')))
                finally:
                        (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    var.get('ctx').callprop('stroke')
    var.get('ctx').put('lineWidth', Js(1.0))
    var.get('ctx').put('strokeStyle', (Js('rgba(0,0,0,0.3)') if var.get('print') else Js('rgba(255,255,255,0.3)')))
    var.get('ctx').callprop('beginPath')
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get(u"this").get('numRows')):
        try:
            var.get('ctx').callprop('moveTo', Js(0.0), (var.get('y')*var.get('tileSize')))
            var.get('ctx').callprop('lineTo', (var.get(u"this").get('widthPixels')-var.get('tileSize')), (var.get('y')*var.get('tileSize')))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('x', Js(0.0))
    while (var.get('x')<var.get(u"this").get('numCols')):
        try:
            var.get('ctx').callprop('moveTo', (var.get('x')*var.get('tileSize')), Js(0.0))
            var.get('ctx').callprop('lineTo', (var.get('x')*var.get('tileSize')), (var.get(u"this").get('heightPixels')-var.get('tileSize')))
        finally:
                (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
    var.get('ctx').callprop('stroke')
    if var.get(u"this").get('name'):
        var.get('ctx').put('fillStyle', (Js('#000') if var.get('print') else Js('#fff')))
        var.get('ctx').put('font', Js('20px sans-serif'))
        var.get('ctx').put('textBaseline', Js('top'))
        var.get('ctx').callprop('fillText', var.get(u"this").get('name'), Js(0.0), (var.get('tileSize')/Js(2.0)))
    var.get('ctx').callprop('restore')
PyJs_anonymous_15_._set_name('anonymous')
var.get('Map').get('prototype').put('drawPath', PyJs_anonymous_15_)
@Js
def PyJs_anonymous_16_(min, max, this, arguments, var=var):
    var = Scope({'min':min, 'max':max, 'this':this, 'arguments':arguments}, var)
    var.registers(['min', 'max'])
    return (var.get('Math').callprop('floor', (var.get('Math').callprop('random')*((var.get('max')-var.get('min'))+Js(1.0))))+var.get('min'))
PyJs_anonymous_16_._set_name('anonymous')
var.put('getRandomInt', PyJs_anonymous_16_)
@Js
def PyJs_anonymous_17_(list, this, arguments, var=var):
    var = Scope({'list':list, 'this':this, 'arguments':arguments}, var)
    var.registers(['j', 'temp', 'list', 'len', 'i'])
    var.put('len', var.get('list').get('length'))
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('len')):
        try:
            var.put('j', var.get('getRandomInt')(Js(0.0), (var.get('len')-Js(1.0))))
            var.put('temp', var.get('list').get(var.get('i')))
            var.get('list').put(var.get('i'), var.get('list').get(var.get('j')))
            var.get('list').put(var.get('j'), var.get('temp'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
PyJs_anonymous_17_._set_name('anonymous')
var.put('shuffle', PyJs_anonymous_17_)
@Js
def PyJs_anonymous_18_(list, this, arguments, var=var):
    var = Scope({'list':list, 'this':this, 'arguments':arguments}, var)
    var.registers(['len', 'list'])
    var.put('len', var.get('list').get('length'))
    if (var.get('len')>Js(0.0)):
        return var.get('list').get(var.get('getRandomInt')(Js(0.0), (var.get('len')-Js(1.0))))
PyJs_anonymous_18_._set_name('anonymous')
var.put('randomElement', PyJs_anonymous_18_)
var.put('UP', Js(0.0))
var.put('RIGHT', Js(1.0))
var.put('DOWN', Js(2.0))
var.put('LEFT', Js(3.0))
var.put('cells', Js([]))
var.put('tallRows', Js([]))
var.put('narrowCols', Js([]))
var.put('rows', Js(9.0))
var.put('cols', Js(5.0))
@Js
def PyJs_anonymous_19_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['c', 'i'])
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('rows')*var.get('cols'))):
        try:
            var.get('cells').put(var.get('i'), Js({'x':(var.get('i')%var.get('cols')),'y':var.get('Math').callprop('floor', (var.get('i')/var.get('cols'))),'filled':Js(False),'connect':Js([Js(False), Js(False), Js(False), Js(False)]),'next':Js([]),'no':var.get('undefined'),'group':var.get('undefined')}))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('rows')*var.get('cols'))):
        try:
            var.put('c', var.get('cells').get(var.get('i')))
            if (var.get('c').get('x')>Js(0.0)):
                var.get('c').get('next').put(var.get('LEFT'), var.get('cells').get((var.get('i')-Js(1.0))))
            if (var.get('c').get('x')<(var.get('cols')-Js(1.0))):
                var.get('c').get('next').put(var.get('RIGHT'), var.get('cells').get((var.get('i')+Js(1.0))))
            if (var.get('c').get('y')>Js(0.0)):
                var.get('c').get('next').put(var.get('UP'), var.get('cells').get((var.get('i')-var.get('cols'))))
            if (var.get('c').get('y')<(var.get('rows')-Js(1.0))):
                var.get('c').get('next').put(var.get('DOWN'), var.get('cells').get((var.get('i')+var.get('cols'))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.put('i', (Js(3.0)*var.get('cols')))
    var.put('c', var.get('cells').get(var.get('i')))
    var.get('c').put('filled', Js(True))
    var.get('c').get('connect').put(var.get('LEFT'), var.get('c').get('connect').put(var.get('RIGHT'), var.get('c').get('connect').put(var.get('DOWN'), Js(True))))
    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.put('c', var.get('cells').get(var.get('i')))
    var.get('c').put('filled', Js(True))
    var.get('c').get('connect').put(var.get('LEFT'), var.get('c').get('connect').put(var.get('DOWN'), Js(True)))
    var.put('i', (var.get('cols')-Js(1.0)), '+')
    var.put('c', var.get('cells').get(var.get('i')))
    var.get('c').put('filled', Js(True))
    var.get('c').get('connect').put(var.get('LEFT'), var.get('c').get('connect').put(var.get('UP'), var.get('c').get('connect').put(var.get('RIGHT'), Js(True))))
    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.put('c', var.get('cells').get(var.get('i')))
    var.get('c').put('filled', Js(True))
    var.get('c').get('connect').put(var.get('UP'), var.get('c').get('connect').put(var.get('LEFT'), Js(True)))
PyJs_anonymous_19_._set_name('anonymous')
var.put('reset', PyJs_anonymous_19_)
@Js
def PyJs_anonymous_20_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['getOpenCells', 'isDesirable', 'connectCell', 'reassignGroup', 'joinWalls', 'createTunnels', 'genCount', 'setUpScaleCoords', 'getLeftMostEmptyCells', 'cellIsCrossCenter', 'isOpenCell', 'chooseNarrowCols', 'gen', 'setResizeCandidates', 'chooseTallRows'])
    @Js
    def PyJs_anonymous_21_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'x', 'leftCells'])
        pass
        var.put('leftCells', Js([]))
        #for JS loop
        var.put('x', Js(0.0))
        while (var.get('x')<var.get('cols')):
            try:
                #for JS loop
                var.put('y', Js(0.0))
                while (var.get('y')<var.get('rows')):
                    try:
                        var.put('c', var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))))
                        if var.get('c').get('filled').neg():
                            var.get('leftCells').callprop('push', var.get('c'))
                    finally:
                            (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
                if (var.get('leftCells').get('length')>Js(0.0)):
                    break
            finally:
                    (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        return var.get('leftCells')
    PyJs_anonymous_21_._set_name('anonymous')
    var.put('getLeftMostEmptyCells', PyJs_anonymous_21_)
    @Js
    def PyJs_anonymous_22_(cell, i, prevDir, size, this, arguments, var=var):
        var = Scope({'cell':cell, 'i':i, 'prevDir':prevDir, 'size':size, 'this':this, 'arguments':arguments}, var)
        var.registers(['cell', 'i', 'prevDir', 'size'])
        if ((((var.get('cell').get('y')==Js(6.0)) and (var.get('cell').get('x')==Js(0.0))) and (var.get('i')==var.get('DOWN'))) or (((var.get('cell').get('y')==Js(7.0)) and (var.get('cell').get('x')==Js(0.0))) and (var.get('i')==var.get('UP')))):
            return Js(False)
        if ((var.get('size')==Js(2.0)) and ((var.get('i')==var.get('prevDir')) or (((var.get('i')+Js(2.0))%Js(4.0))==var.get('prevDir')))):
            return Js(False)
        if (var.get('cell').get('next').get(var.get('i')) and var.get('cell').get('next').get(var.get('i')).get('filled').neg()):
            if (var.get('cell').get('next').get(var.get('i')).get('next').get(var.get('LEFT')) and var.get('cell').get('next').get(var.get('i')).get('next').get(var.get('LEFT')).get('filled').neg()):
                pass
            else:
                return Js(True)
        return Js(False)
    PyJs_anonymous_22_._set_name('anonymous')
    var.put('isOpenCell', PyJs_anonymous_22_)
    @Js
    def PyJs_anonymous_23_(cell, prevDir, size, this, arguments, var=var):
        var = Scope({'cell':cell, 'prevDir':prevDir, 'size':size, 'this':this, 'arguments':arguments}, var)
        var.registers(['cell', 'prevDir', 'openCells', 'numOpenCells', 'size'])
        var.put('openCells', Js([]))
        var.put('numOpenCells', Js(0.0))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<Js(4.0)):
            try:
                if var.get('isOpenCell')(var.get('cell'), var.get('i'), var.get('prevDir'), var.get('size')):
                    var.get('openCells').callprop('push', var.get('i'))
                    (var.put('numOpenCells',Js(var.get('numOpenCells').to_number())+Js(1))-Js(1))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        return Js({'openCells':var.get('openCells'),'numOpenCells':var.get('numOpenCells')})
    PyJs_anonymous_23_._set_name('anonymous')
    var.put('getOpenCells', PyJs_anonymous_23_)
    @Js
    def PyJs_anonymous_24_(cell, dir, this, arguments, var=var):
        var = Scope({'cell':cell, 'dir':dir, 'this':this, 'arguments':arguments}, var)
        var.registers(['cell', 'dir'])
        var.get('cell').get('connect').put(var.get('dir'), Js(True))
        var.get('cell').get('next').get(var.get('dir')).get('connect').put(((var.get('dir')+Js(2.0))%Js(4.0)), Js(True))
        if ((var.get('cell').get('x')==Js(0.0)) and (var.get('dir')==var.get('RIGHT'))):
            var.get('cell').get('connect').put(var.get('LEFT'), Js(True))
    PyJs_anonymous_24_._set_name('anonymous')
    var.put('connectCell', PyJs_anonymous_24_)
    @Js
    def PyJs_anonymous_25_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['singleCount', 'newCell', 'numFilled', 'stop', 'probStopGrowingAtSize', 'size', 'probExtendAtSize3or4', 'probTopAndBotSingleCellJoin', 'i', 'longPieces', 'cell', 'result', 'firstCell', 'openCells', 'dirs', 'maxLongPieces', 'dirsLength', 'dir', 'numOpenCells', 'fillCell', 'numGroups', 'c', 'probExtendAtSize2'])
        pass
        pass
        pass
        pass
        pass
        pass
        pass
        var.put('numFilled', Js(0.0))
        pass
        pass
        var.put('probStopGrowingAtSize', Js([Js(0.0), Js(0.0), Js(0.1), Js(0.5), Js(0.75), Js(1.0)]))
        var.put('singleCount', Js({}))
        var.get('singleCount').put('0', var.get('singleCount').put((var.get('rows')-Js(1.0)), Js(0.0)))
        var.put('probTopAndBotSingleCellJoin', Js(0.35))
        var.put('longPieces', Js(0.0))
        var.put('maxLongPieces', Js(1.0))
        var.put('probExtendAtSize2', Js(1.0))
        var.put('probExtendAtSize3or4', Js(0.5))
        @Js
        def PyJs_anonymous_26_(cell, this, arguments, var=var):
            var = Scope({'cell':cell, 'this':this, 'arguments':arguments}, var)
            var.registers(['cell'])
            var.get('cell').put('filled', Js(True))
            var.get('cell').put('no', (var.put('numFilled',Js(var.get('numFilled').to_number())+Js(1))-Js(1)))
            var.get('cell').put('group', var.get('numGroups'))
        PyJs_anonymous_26_._set_name('anonymous')
        var.put('fillCell', PyJs_anonymous_26_)
        #for JS loop
        var.put('numGroups', Js(0.0))
        while 1:
            try:
                var.put('openCells', var.get('getLeftMostEmptyCells')())
                var.put('numOpenCells', var.get('openCells').get('length'))
                if (var.get('numOpenCells')==Js(0.0)):
                    break
                var.put('firstCell', var.put('cell', var.get('openCells').get(var.get('getRandomInt')(Js(0.0), (var.get('numOpenCells')-Js(1.0))))))
                var.get('fillCell')(var.get('cell'))
                if (((var.get('cell').get('x')<(var.get('cols')-Js(1.0))) and var.get('singleCount').contains(var.get('cell').get('y'))) and (var.get('Math').callprop('random')<=var.get('probTopAndBotSingleCellJoin'))):
                    if (var.get('singleCount').get(var.get('cell').get('y'))==Js(0.0)):
                        var.get('cell').get('connect').put((var.get('UP') if (var.get('cell').get('y')==Js(0.0)) else var.get('DOWN')), Js(True))
                        (var.get('singleCount').put(var.get('cell').get('y'),Js(var.get('singleCount').get(var.get('cell').get('y')).to_number())+Js(1))-Js(1))
                        continue
                var.put('size', Js(1.0))
                if (var.get('cell').get('x')==(var.get('cols')-Js(1.0))):
                    var.get('cell').get('connect').put(var.get('RIGHT'), Js(True))
                    var.get('cell').put('isRaiseHeightCandidate', Js(True))
                else:
                    while (var.get('size')<Js(5.0)):
                        var.put('stop', Js(False))
                        if (var.get('size')==Js(2.0)):
                            var.put('c', var.get('firstCell'))
                            if ((((var.get('c').get('x')>Js(0.0)) and var.get('c').get('connect').get(var.get('RIGHT'))) and var.get('c').get('next').get(var.get('RIGHT'))) and var.get('c').get('next').get(var.get('RIGHT')).get('next').get(var.get('RIGHT'))):
                                if ((var.get('longPieces')<var.get('maxLongPieces')) and (var.get('Math').callprop('random')<=var.get('probExtendAtSize2'))):
                                    var.put('c', var.get('c').get('next').get(var.get('RIGHT')).get('next').get(var.get('RIGHT')))
                                    var.put('dirs', Js({}))
                                    if var.get('isOpenCell')(var.get('c'), var.get('UP')):
                                        var.get('dirs').put(var.get('UP'), Js(True))
                                    if var.get('isOpenCell')(var.get('c'), var.get('DOWN')):
                                        var.get('dirs').put(var.get('DOWN'), Js(True))
                                    if (var.get('dirs').get(var.get('UP')) and var.get('dirs').get(var.get('DOWN'))):
                                        var.put('i', Js([var.get('UP'), var.get('DOWN')]).get(var.get('getRandomInt')(Js(0.0), Js(1.0))))
                                    else:
                                        if var.get('dirs').get(var.get('UP')):
                                            var.put('i', var.get('UP'))
                                        else:
                                            if var.get('dirs').get(var.get('DOWN')):
                                                var.put('i', var.get('DOWN'))
                                            else:
                                                var.put('i', var.get('undefined'))
                                    if (var.get('i')!=var.get('undefined')):
                                        var.get('connectCell')(var.get('c'), var.get('LEFT'))
                                        var.get('fillCell')(var.get('c'))
                                        var.get('connectCell')(var.get('c'), var.get('i'))
                                        var.get('fillCell')(var.get('c').get('next').get(var.get('i')))
                                        (var.put('longPieces',Js(var.get('longPieces').to_number())+Js(1))-Js(1))
                                        var.put('size', Js(2.0), '+')
                                        var.put('stop', Js(True))
                        if var.get('stop').neg():
                            var.put('result', var.get('getOpenCells')(var.get('cell'), var.get('dir'), var.get('size')))
                            var.put('openCells', var.get('result').get('openCells'))
                            var.put('numOpenCells', var.get('result').get('numOpenCells'))
                            if ((var.get('numOpenCells')==Js(0.0)) and (var.get('size')==Js(2.0))):
                                var.put('cell', var.get('newCell'))
                                var.put('result', var.get('getOpenCells')(var.get('cell'), var.get('dir'), var.get('size')))
                                var.put('openCells', var.get('result').get('openCells'))
                                var.put('numOpenCells', var.get('result').get('numOpenCells'))
                            if (var.get('numOpenCells')==Js(0.0)):
                                var.put('stop', Js(True))
                            else:
                                var.put('dir', var.get('openCells').get(var.get('getRandomInt')(Js(0.0), (var.get('numOpenCells')-Js(1.0)))))
                                var.put('newCell', var.get('cell').get('next').get(var.get('dir')))
                                var.get('connectCell')(var.get('cell'), var.get('dir'))
                                var.get('fillCell')(var.get('newCell'))
                                (var.put('size',Js(var.get('size').to_number())+Js(1))-Js(1))
                                if ((var.get('firstCell').get('x')==Js(0.0)) and (var.get('size')==Js(3.0))):
                                    var.put('stop', Js(True))
                                if (var.get('Math').callprop('random')<=var.get('probStopGrowingAtSize').get(var.get('size'))):
                                    var.put('stop', Js(True))
                        if var.get('stop'):
                            if (var.get('size')==Js(1.0)):
                                pass
                            else:
                                if (var.get('size')==Js(2.0)):
                                    var.put('c', var.get('firstCell'))
                                    if (var.get('c').get('x')==(var.get('cols')-Js(1.0))):
                                        if var.get('c').get('connect').get(var.get('UP')):
                                            var.put('c', var.get('c').get('next').get(var.get('UP')))
                                        var.get('c').get('connect').put(var.get('RIGHT'), var.get('c').get('next').get(var.get('DOWN')).get('connect').put(var.get('RIGHT'), Js(True)))
                                else:
                                    if ((var.get('size')==Js(3.0)) or (var.get('size')==Js(4.0))):
                                        if (((var.get('longPieces')<var.get('maxLongPieces')) and (var.get('firstCell').get('x')>Js(0.0))) and (var.get('Math').callprop('random')<=var.get('probExtendAtSize3or4'))):
                                            var.put('dirs', Js([]))
                                            var.put('dirsLength', Js(0.0))
                                            #for JS loop
                                            var.put('i', Js(0.0))
                                            while (var.get('i')<Js(4.0)):
                                                try:
                                                    if (var.get('cell').get('connect').get(var.get('i')) and var.get('isOpenCell')(var.get('cell').get('next').get(var.get('i')), var.get('i'))):
                                                        var.get('dirs').callprop('push', var.get('i'))
                                                        (var.put('dirsLength',Js(var.get('dirsLength').to_number())+Js(1))-Js(1))
                                                finally:
                                                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
                                            if (var.get('dirsLength')>Js(0.0)):
                                                var.put('i', var.get('dirs').get(var.get('getRandomInt')(Js(0.0), (var.get('dirsLength')-Js(1.0)))))
                                                var.put('c', var.get('cell').get('next').get(var.get('i')))
                                                var.get('connectCell')(var.get('c'), var.get('i'))
                                                var.get('fillCell')(var.get('c').get('next').get(var.get('i')))
                                                (var.put('longPieces',Js(var.get('longPieces').to_number())+Js(1))-Js(1))
                            break
            finally:
                    (var.put('numGroups',Js(var.get('numGroups').to_number())+Js(1))-Js(1))
        var.get('setResizeCandidates')()
    PyJs_anonymous_25_._set_name('anonymous')
    var.put('gen', PyJs_anonymous_25_)
    @Js
    def PyJs_anonymous_27_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['q2', 'c2', 'x', 'y', 'c', 'q', 'i'])
        pass
        pass
        pass
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<(var.get('rows')*var.get('cols'))):
            try:
                var.put('c', var.get('cells').get(var.get('i')))
                var.put('x', (var.get('i')%var.get('cols')))
                var.put('y', var.get('Math').callprop('floor', (var.get('i')/var.get('cols'))))
                var.put('q', var.get('c').get('connect'))
                if ((((var.get('c').get('x')==Js(0.0)) or var.get('q').get(var.get('LEFT')).neg()) and ((var.get('c').get('x')==(var.get('cols')-Js(1.0))) or var.get('q').get(var.get('RIGHT')).neg())) and (var.get('q').get(var.get('UP'))!=var.get('q').get(var.get('DOWN')))):
                    var.get('c').put('isRaiseHeightCandidate', Js(True))
                var.put('c2', var.get('c').get('next').get(var.get('RIGHT')))
                if (var.get('c2')!=var.get('undefined')):
                    var.put('q2', var.get('c2').get('connect'))
                    if (((((var.get('c').get('x')==Js(0.0)) or var.get('q').get(var.get('LEFT')).neg()) and var.get('q').get(var.get('UP')).neg()) and var.get('q').get(var.get('DOWN')).neg()) and ((((var.get('c2').get('x')==(var.get('cols')-Js(1.0))) or var.get('q2').get(var.get('RIGHT')).neg()) and var.get('q2').get(var.get('UP')).neg()) and var.get('q2').get(var.get('DOWN')).neg())):
                        var.get('c').put('isRaiseHeightCandidate', var.get('c2').put('isRaiseHeightCandidate', Js(True)))
                if ((var.get('c').get('x')==(var.get('cols')-Js(1.0))) and var.get('q').get(var.get('RIGHT'))):
                    var.get('c').put('isShrinkWidthCandidate', Js(True))
                if ((((var.get('c').get('y')==Js(0.0)) or var.get('q').get(var.get('UP')).neg()) and ((var.get('c').get('y')==(var.get('rows')-Js(1.0))) or var.get('q').get(var.get('DOWN')).neg())) and (var.get('q').get(var.get('LEFT'))!=var.get('q').get(var.get('RIGHT')))):
                    var.get('c').put('isShrinkWidthCandidate', Js(True))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJs_anonymous_27_._set_name('anonymous')
    var.put('setResizeCandidates', PyJs_anonymous_27_)
    @Js
    def PyJs_anonymous_28_(c, this, arguments, var=var):
        var = Scope({'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['c'])
        return (((var.get('c').get('connect').get(var.get('UP')) and var.get('c').get('connect').get(var.get('RIGHT'))) and var.get('c').get('connect').get(var.get('DOWN'))) and var.get('c').get('connect').get(var.get('LEFT')))
    PyJs_anonymous_28_._set_name('anonymous')
    var.put('cellIsCrossCenter', PyJs_anonymous_28_)
    @Js
    def PyJs_anonymous_29_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'canShrinkWidth', 'x'])
        @Js
        def PyJs_anonymous_30_(x, y, this, arguments, var=var):
            var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
            var.registers(['candidates', 'numCandidates', 'x0', 'c2', 'x', 'y', 'c', 'i'])
            if (var.get('y')==(var.get('rows')-Js(1.0))):
                return Js(True)
            pass
            pass
            #for JS loop
            var.put('x0', var.get('x'))
            while (var.get('x0')<var.get('cols')):
                try:
                    var.put('c', var.get('cells').get((var.get('x0')+(var.get('y')*var.get('cols')))))
                    var.put('c2', var.get('c').get('next').get(var.get('DOWN')))
                    if ((var.get('c').get('connect').get(var.get('RIGHT')).neg() or var.get('cellIsCrossCenter')(var.get('c'))) and (var.get('c2').get('connect').get(var.get('RIGHT')).neg() or var.get('cellIsCrossCenter')(var.get('c2')))):
                        break
                finally:
                        (var.put('x0',Js(var.get('x0').to_number())+Js(1))-Js(1))
            var.put('candidates', Js([]))
            var.put('numCandidates', Js(0.0))
            #for JS loop
            
            while var.get('c2'):
                try:
                    if var.get('c2').get('isShrinkWidthCandidate'):
                        var.get('candidates').callprop('push', var.get('c2'))
                        (var.put('numCandidates',Js(var.get('numCandidates').to_number())+Js(1))-Js(1))
                    if ((var.get('c2').get('connect').get(var.get('LEFT')).neg() or var.get('cellIsCrossCenter')(var.get('c2'))) and (var.get('c2').get('next').get(var.get('UP')).get('connect').get(var.get('LEFT')).neg() or var.get('cellIsCrossCenter')(var.get('c2').get('next').get(var.get('UP'))))):
                        break
                finally:
                        var.put('c2', var.get('c2').get('next').get(var.get('LEFT')))
            var.get('shuffle')(var.get('candidates'))
            pass
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('numCandidates')):
                try:
                    var.put('c2', var.get('candidates').get(var.get('i')))
                    if var.get('canShrinkWidth')(var.get('c2').get('x'), var.get('c2').get('y')):
                        var.get('c2').put('shrinkWidth', Js(True))
                        var.get('narrowCols').put(var.get('c2').get('y'), var.get('c2').get('x'))
                        return Js(True)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(False)
        PyJs_anonymous_30_._set_name('anonymous')
        var.put('canShrinkWidth', PyJs_anonymous_30_)
        pass
        pass
        #for JS loop
        var.put('x', (var.get('cols')-Js(1.0)))
        while (var.get('x')>=Js(0.0)):
            try:
                var.put('c', var.get('cells').get(var.get('x')))
                if (var.get('c').get('isShrinkWidthCandidate') and var.get('canShrinkWidth')(var.get('x'), Js(0.0))):
                    var.get('c').put('shrinkWidth', Js(True))
                    var.get('narrowCols').put(var.get('c').get('y'), var.get('c').get('x'))
                    return Js(True)
            finally:
                    (var.put('x',Js(var.get('x').to_number())-Js(1))+Js(1))
        return Js(False)
    PyJs_anonymous_29_._set_name('anonymous')
    var.put('chooseNarrowCols', PyJs_anonymous_29_)
    @Js
    def PyJs_anonymous_31_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'canRaiseHeight', 'y'])
        @Js
        def PyJs_anonymous_32_(x, y, this, arguments, var=var):
            var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
            var.registers(['candidates', 'numCandidates', 'y0', 'c2', 'x', 'y', 'c', 'i'])
            if (var.get('x')==(var.get('cols')-Js(1.0))):
                return Js(True)
            pass
            pass
            pass
            #for JS loop
            var.put('y0', var.get('y'))
            while (var.get('y0')>=Js(0.0)):
                try:
                    var.put('c', var.get('cells').get((var.get('x')+(var.get('y0')*var.get('cols')))))
                    var.put('c2', var.get('c').get('next').get(var.get('RIGHT')))
                    if ((var.get('c').get('connect').get(var.get('UP')).neg() or var.get('cellIsCrossCenter')(var.get('c'))) and (var.get('c2').get('connect').get(var.get('UP')).neg() or var.get('cellIsCrossCenter')(var.get('c2')))):
                        break
                finally:
                        (var.put('y0',Js(var.get('y0').to_number())-Js(1))+Js(1))
            var.put('candidates', Js([]))
            var.put('numCandidates', Js(0.0))
            #for JS loop
            
            while var.get('c2'):
                try:
                    if var.get('c2').get('isRaiseHeightCandidate'):
                        var.get('candidates').callprop('push', var.get('c2'))
                        (var.put('numCandidates',Js(var.get('numCandidates').to_number())+Js(1))-Js(1))
                    if ((var.get('c2').get('connect').get(var.get('DOWN')).neg() or var.get('cellIsCrossCenter')(var.get('c2'))) and (var.get('c2').get('next').get(var.get('LEFT')).get('connect').get(var.get('DOWN')).neg() or var.get('cellIsCrossCenter')(var.get('c2').get('next').get(var.get('LEFT'))))):
                        break
                finally:
                        var.put('c2', var.get('c2').get('next').get(var.get('DOWN')))
            var.get('shuffle')(var.get('candidates'))
            pass
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('numCandidates')):
                try:
                    var.put('c2', var.get('candidates').get(var.get('i')))
                    if var.get('canRaiseHeight')(var.get('c2').get('x'), var.get('c2').get('y')):
                        var.get('c2').put('raiseHeight', Js(True))
                        var.get('tallRows').put(var.get('c2').get('x'), var.get('c2').get('y'))
                        return Js(True)
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js(False)
        PyJs_anonymous_32_._set_name('anonymous')
        var.put('canRaiseHeight', PyJs_anonymous_32_)
        pass
        pass
        #for JS loop
        var.put('y', Js(0.0))
        while (var.get('y')<Js(3.0)):
            try:
                var.put('c', var.get('cells').get((var.get('y')*var.get('cols'))))
                if (var.get('c').get('isRaiseHeightCandidate') and var.get('canRaiseHeight')(Js(0.0), var.get('y'))):
                    var.get('c').put('raiseHeight', Js(True))
                    var.get('tallRows').put(var.get('c').get('x'), var.get('c').get('y'))
                    return Js(True)
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        return Js(False)
    PyJs_anonymous_31_._set_name('anonymous')
    var.put('chooseTallRows', PyJs_anonymous_31_)
    @Js
    def PyJs_anonymous_33_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['isVert', 'x', 'g', 'isHori', 'y', 'c'])
        var.put('c', var.get('cells').get('4'))
        if (var.get('c').get('connect').get(var.get('UP')) or var.get('c').get('connect').get(var.get('RIGHT'))):
            return Js(False)
        var.put('c', var.get('cells').get(((var.get('rows')*var.get('cols'))-Js(1.0))))
        if (var.get('c').get('connect').get(var.get('DOWN')) or var.get('c').get('connect').get(var.get('RIGHT'))):
            return Js(False)
        @Js
        def PyJs_anonymous_34_(x, y, this, arguments, var=var):
            var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
            var.registers(['q2', 'q1', 'x', 'y'])
            var.put('q1', var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))).get('connect'))
            var.put('q2', var.get('cells').get(((var.get('x')+Js(1.0))+(var.get('y')*var.get('cols')))).get('connect'))
            return (((((((var.get('q1').get(var.get('UP')).neg() and var.get('q1').get(var.get('DOWN')).neg()) and ((var.get('x')==Js(0.0)) or var.get('q1').get(var.get('LEFT')).neg())) and var.get('q1').get(var.get('RIGHT'))) and var.get('q2').get(var.get('UP')).neg()) and var.get('q2').get(var.get('DOWN')).neg()) and var.get('q2').get(var.get('LEFT'))) and var.get('q2').get(var.get('RIGHT')).neg())
        PyJs_anonymous_34_._set_name('anonymous')
        var.put('isHori', PyJs_anonymous_34_)
        @Js
        def PyJs_anonymous_35_(x, y, this, arguments, var=var):
            var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
            var.registers(['q2', 'q1', 'x', 'y'])
            var.put('q1', var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))).get('connect'))
            var.put('q2', var.get('cells').get((var.get('x')+((var.get('y')+Js(1.0))*var.get('cols')))).get('connect'))
            if (var.get('x')==(var.get('cols')-Js(1.0))):
                return (((((var.get('q1').get(var.get('LEFT')).neg() and var.get('q1').get(var.get('UP')).neg()) and var.get('q1').get(var.get('DOWN')).neg()) and var.get('q2').get(var.get('LEFT')).neg()) and var.get('q2').get(var.get('UP')).neg()) and var.get('q2').get(var.get('DOWN')).neg())
            return (((((((var.get('q1').get(var.get('LEFT')).neg() and var.get('q1').get(var.get('RIGHT')).neg()) and var.get('q1').get(var.get('UP')).neg()) and var.get('q1').get(var.get('DOWN'))) and var.get('q2').get(var.get('LEFT')).neg()) and var.get('q2').get(var.get('RIGHT')).neg()) and var.get('q2').get(var.get('UP'))) and var.get('q2').get(var.get('DOWN')).neg())
        PyJs_anonymous_35_._set_name('anonymous')
        var.put('isVert', PyJs_anonymous_35_)
        pass
        pass
        #for JS loop
        var.put('y', Js(0.0))
        while (var.get('y')<(var.get('rows')-Js(1.0))):
            try:
                #for JS loop
                var.put('x', Js(0.0))
                while (var.get('x')<(var.get('cols')-Js(1.0))):
                    try:
                        if ((var.get('isHori')(var.get('x'), var.get('y')) and var.get('isHori')(var.get('x'), (var.get('y')+Js(1.0)))) or (var.get('isVert')(var.get('x'), var.get('y')) and var.get('isVert')((var.get('x')+Js(1.0)), var.get('y')))):
                            if (var.get('x')==Js(0.0)):
                                return Js(False)
                            var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))).get('connect').put(var.get('DOWN'), Js(True))
                            var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))).get('connect').put(var.get('RIGHT'), Js(True))
                            var.put('g', var.get('cells').get((var.get('x')+(var.get('y')*var.get('cols')))).get('group'))
                            var.get('cells').get(((var.get('x')+Js(1.0))+(var.get('y')*var.get('cols')))).get('connect').put(var.get('DOWN'), Js(True))
                            var.get('cells').get(((var.get('x')+Js(1.0))+(var.get('y')*var.get('cols')))).get('connect').put(var.get('LEFT'), Js(True))
                            var.get('cells').get(((var.get('x')+Js(1.0))+(var.get('y')*var.get('cols')))).put('group', var.get('g'))
                            var.get('cells').get((var.get('x')+((var.get('y')+Js(1.0))*var.get('cols')))).get('connect').put(var.get('UP'), Js(True))
                            var.get('cells').get((var.get('x')+((var.get('y')+Js(1.0))*var.get('cols')))).get('connect').put(var.get('RIGHT'), Js(True))
                            var.get('cells').get((var.get('x')+((var.get('y')+Js(1.0))*var.get('cols')))).put('group', var.get('g'))
                            var.get('cells').get(((var.get('x')+Js(1.0))+((var.get('y')+Js(1.0))*var.get('cols')))).get('connect').put(var.get('UP'), Js(True))
                            var.get('cells').get(((var.get('x')+Js(1.0))+((var.get('y')+Js(1.0))*var.get('cols')))).get('connect').put(var.get('LEFT'), Js(True))
                            var.get('cells').get(((var.get('x')+Js(1.0))+((var.get('y')+Js(1.0))*var.get('cols')))).put('group', var.get('g'))
                    finally:
                            (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        if var.get('chooseTallRows')().neg():
            return Js(False)
        if var.get('chooseNarrowCols')().neg():
            return Js(False)
        return Js(True)
    PyJs_anonymous_33_._set_name('anonymous')
    var.put('isDesirable', PyJs_anonymous_33_)
    @Js
    def PyJs_anonymous_36_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'i'])
        pass
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<(var.get('rows')*var.get('cols'))):
            try:
                var.put('c', var.get('cells').get(var.get('i')))
                var.get('c').put('final_x', (var.get('c').get('x')*Js(3.0)))
                if (var.get('narrowCols').get(var.get('c').get('y'))<var.get('c').get('x')):
                    (var.get('c').put('final_x',Js(var.get('c').get('final_x').to_number())-Js(1))+Js(1))
                var.get('c').put('final_y', (var.get('c').get('y')*Js(3.0)))
                if (var.get('tallRows').get(var.get('c').get('x'))<var.get('c').get('y')):
                    (var.get('c').put('final_y',Js(var.get('c').get('final_y').to_number())+Js(1))-Js(1))
                var.get('c').put('final_w', (Js(2.0) if var.get('c').get('shrinkWidth') else Js(3.0)))
                var.get('c').put('final_h', (Js(4.0) if var.get('c').get('raiseHeight') else Js(3.0)))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJs_anonymous_36_._set_name('anonymous')
    var.put('setUpScaleCoords', PyJs_anonymous_36_)
    @Js
    def PyJs_anonymous_37_(oldg, newg, this, arguments, var=var):
        var = Scope({'oldg':oldg, 'newg':newg, 'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'i', 'oldg', 'newg'])
        pass
        pass
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<(var.get('rows')*var.get('cols'))):
            try:
                var.put('c', var.get('cells').get(var.get('i')))
                if (var.get('c').get('group')==var.get('oldg')):
                    var.get('c').put('group', var.get('newg'))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    PyJs_anonymous_37_._set_name('anonymous')
    var.put('reassignGroup', PyJs_anonymous_37_)
    @Js
    def PyJs_anonymous_38_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['downDead', 'numTunnelsDesired', 'voidTunnelCells', 'singleDeadEndCells', 'topy', 'doubleDeadEndCells', 'topSingleDeadEndCells', 'numTunnelsCreated', 'y', 'botEdgeTunnelCells', 'len', 'selectSingleDeadEnd', 'botVoidTunnelCells', 'i', 'botSingleDeadEndCells', 'topEdgeTunnelCells', 'topVoidTunnelCells', 'offset', 'edgeTunnelCells', 'replaceGroup', 'c', 'exit', 'upDead'])
        var.put('singleDeadEndCells', Js([]))
        var.put('topSingleDeadEndCells', Js([]))
        var.put('botSingleDeadEndCells', Js([]))
        var.put('voidTunnelCells', Js([]))
        var.put('topVoidTunnelCells', Js([]))
        var.put('botVoidTunnelCells', Js([]))
        var.put('edgeTunnelCells', Js([]))
        var.put('topEdgeTunnelCells', Js([]))
        var.put('botEdgeTunnelCells', Js([]))
        var.put('doubleDeadEndCells', Js([]))
        var.put('numTunnelsCreated', Js(0.0))
        pass
        pass
        pass
        pass
        #for JS loop
        var.put('y', Js(0.0))
        while (var.get('y')<var.get('rows')):
            try:
                var.put('c', var.get('cells').get(((var.get('cols')-Js(1.0))+(var.get('y')*var.get('cols')))))
                if var.get('c').get('connect').get(var.get('UP')):
                    continue
                if ((var.get('c').get('y')>Js(1.0)) and (var.get('c').get('y')<(var.get('rows')-Js(2.0)))):
                    var.get('c').put('isEdgeTunnelCandidate', Js(True))
                    var.get('edgeTunnelCells').callprop('push', var.get('c'))
                    if (var.get('c').get('y')<=Js(2.0)):
                        var.get('topEdgeTunnelCells').callprop('push', var.get('c'))
                    else:
                        if (var.get('c').get('y')>=Js(5.0)):
                            var.get('botEdgeTunnelCells').callprop('push', var.get('c'))
                var.put('upDead', (var.get('c').get('next').get(var.get('UP')).neg() or var.get('c').get('next').get(var.get('UP')).get('connect').get(var.get('RIGHT'))))
                var.put('downDead', (var.get('c').get('next').get(var.get('DOWN')).neg() or var.get('c').get('next').get(var.get('DOWN')).get('connect').get(var.get('RIGHT'))))
                if var.get('c').get('connect').get(var.get('RIGHT')):
                    if var.get('upDead'):
                        var.get('c').put('isVoidTunnelCandidate', Js(True))
                        var.get('voidTunnelCells').callprop('push', var.get('c'))
                        if (var.get('c').get('y')<=Js(2.0)):
                            var.get('topVoidTunnelCells').callprop('push', var.get('c'))
                        else:
                            if (var.get('c').get('y')>=Js(6.0)):
                                var.get('botVoidTunnelCells').callprop('push', var.get('c'))
                else:
                    if var.get('c').get('connect').get(var.get('DOWN')):
                        continue
                    if (var.get('upDead')!=var.get('downDead')):
                        if ((var.get('c').get('raiseHeight').neg() and (var.get('y')<(var.get('rows')-Js(1.0)))) and var.get('c').get('next').get(var.get('LEFT')).get('connect').get(var.get('LEFT')).neg()):
                            var.get('singleDeadEndCells').callprop('push', var.get('c'))
                            var.get('c').put('isSingleDeadEndCandidate', Js(True))
                            var.get('c').put('singleDeadEndDir', (var.get('UP') if var.get('upDead') else var.get('DOWN')))
                            var.put('offset', (Js(1.0) if var.get('upDead') else Js(0.0)))
                            if (var.get('c').get('y')<=(Js(1.0)+var.get('offset'))):
                                var.get('topSingleDeadEndCells').callprop('push', var.get('c'))
                            else:
                                if (var.get('c').get('y')>=(Js(5.0)+var.get('offset'))):
                                    var.get('botSingleDeadEndCells').callprop('push', var.get('c'))
                    else:
                        if (var.get('upDead') and var.get('downDead')):
                            if ((var.get('y')>Js(0.0)) and (var.get('y')<(var.get('rows')-Js(1.0)))):
                                if (var.get('c').get('next').get(var.get('LEFT')).get('connect').get(var.get('UP')) and var.get('c').get('next').get(var.get('LEFT')).get('connect').get(var.get('DOWN'))):
                                    var.get('c').put('isDoubleDeadEndCandidate', Js(True))
                                    if ((var.get('c').get('y')>=Js(2.0)) and (var.get('c').get('y')<=Js(5.0))):
                                        var.get('doubleDeadEndCells').callprop('push', var.get('c'))
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        var.put('numTunnelsDesired', (Js(2.0) if (var.get('Math').callprop('random')<=Js(0.45)) else Js(1.0)))
        pass
        @Js
        def PyJs_anonymous_39_(c, this, arguments, var=var):
            var = Scope({'c':c, 'this':this, 'arguments':arguments}, var)
            var.registers(['c'])
            var.get('c').get('connect').put(var.get('RIGHT'), Js(True))
            if (var.get('c').get('singleDeadEndDir')==var.get('UP')):
                var.get('c').put('topTunnel', Js(True))
            else:
                var.get('c').get('next').get(var.get('DOWN')).put('topTunnel', Js(True))
        PyJs_anonymous_39_._set_name('anonymous')
        var.put('selectSingleDeadEnd', PyJs_anonymous_39_)
        if (var.get('numTunnelsDesired')==Js(1.0)):
            if var.put('c', var.get('randomElement')(var.get('voidTunnelCells'))):
                var.get('c').put('topTunnel', Js(True))
            else:
                if var.put('c', var.get('randomElement')(var.get('singleDeadEndCells'))):
                    var.get('selectSingleDeadEnd')(var.get('c'))
                else:
                    if var.put('c', var.get('randomElement')(var.get('edgeTunnelCells'))):
                        var.get('c').put('topTunnel', Js(True))
                    else:
                        return Js(False)
        else:
            if (var.get('numTunnelsDesired')==Js(2.0)):
                if var.put('c', var.get('randomElement')(var.get('doubleDeadEndCells'))):
                    var.get('c').get('connect').put(var.get('RIGHT'), Js(True))
                    var.get('c').put('topTunnel', Js(True))
                    var.get('c').get('next').get(var.get('DOWN')).put('topTunnel', Js(True))
                else:
                    var.put('numTunnelsCreated', Js(1.0))
                    if var.put('c', var.get('randomElement')(var.get('topVoidTunnelCells'))):
                        var.get('c').put('topTunnel', Js(True))
                    else:
                        if var.put('c', var.get('randomElement')(var.get('topSingleDeadEndCells'))):
                            var.get('selectSingleDeadEnd')(var.get('c'))
                        else:
                            if var.put('c', var.get('randomElement')(var.get('topEdgeTunnelCells'))):
                                var.get('c').put('topTunnel', Js(True))
                            else:
                                var.put('numTunnelsCreated', Js(0.0))
                    if var.put('c', var.get('randomElement')(var.get('botVoidTunnelCells'))):
                        var.get('c').put('topTunnel', Js(True))
                    else:
                        if var.put('c', var.get('randomElement')(var.get('botSingleDeadEndCells'))):
                            var.get('selectSingleDeadEnd')(var.get('c'))
                        else:
                            if var.put('c', var.get('randomElement')(var.get('botEdgeTunnelCells'))):
                                var.get('c').put('topTunnel', Js(True))
                            else:
                                if (var.get('numTunnelsCreated')==Js(0.0)):
                                    return Js(False)
        pass
        #for JS loop
        var.put('y', Js(0.0))
        while (var.get('y')<var.get('rows')):
            try:
                var.put('c', var.get('cells').get(((var.get('cols')-Js(1.0))+(var.get('y')*var.get('cols')))))
                if var.get('c').get('topTunnel'):
                    var.put('exit', Js(True))
                    var.put('topy', var.get('c').get('final_y'))
                    while var.get('c').get('next').get(var.get('LEFT')):
                        var.put('c', var.get('c').get('next').get(var.get('LEFT')))
                        if (var.get('c').get('connect').get(var.get('UP')).neg() and (var.get('c').get('final_y')==var.get('topy'))):
                            continue
                        else:
                            var.put('exit', Js(False))
                            break
                    if var.get('exit'):
                        return Js(False)
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        var.put('len', var.get('voidTunnelCells').get('length'))
        pass
        @Js
        def PyJs_anonymous_40_(oldg, newg, this, arguments, var=var):
            var = Scope({'oldg':oldg, 'newg':newg, 'this':this, 'arguments':arguments}, var)
            var.registers(['c', 'i', 'oldg', 'newg'])
            pass
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<(var.get('rows')*var.get('cols'))):
                try:
                    var.put('c', var.get('cells').get(var.get('i')))
                    if (var.get('c').get('group')==var.get('oldg')):
                        var.get('c').put('group', var.get('newg'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        PyJs_anonymous_40_._set_name('anonymous')
        var.put('replaceGroup', PyJs_anonymous_40_)
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('len')):
            try:
                var.put('c', var.get('voidTunnelCells').get(var.get('i')))
                if var.get('c').get('topTunnel').neg():
                    var.get('replaceGroup')(var.get('c').get('group'), var.get('c').get('next').get(var.get('UP')).get('group'))
                    var.get('c').get('connect').put(var.get('UP'), Js(True))
                    var.get('c').get('next').get(var.get('UP')).get('connect').put(var.get('DOWN'), Js(True))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        return Js(True)
    PyJs_anonymous_38_._set_name('anonymous')
    var.put('createTunnels', PyJs_anonymous_38_)
    @Js
    def PyJs_anonymous_41_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['c', 'c2', 'x', 'y'])
        pass
        pass
        #for JS loop
        var.put('x', Js(0.0))
        while (var.get('x')<var.get('cols')):
            try:
                var.put('c', var.get('cells').get(var.get('x')))
                if (((var.get('c').get('connect').get(var.get('LEFT')).neg() and var.get('c').get('connect').get(var.get('RIGHT')).neg()) and var.get('c').get('connect').get(var.get('UP')).neg()) and (var.get('c').get('connect').get(var.get('DOWN')).neg() or var.get('c').get('next').get(var.get('DOWN')).get('connect').get(var.get('DOWN')).neg())):
                    if ((var.get('c').get('next').get(var.get('LEFT')).neg() or var.get('c').get('next').get(var.get('LEFT')).get('connect').get(var.get('UP')).neg()) and (var.get('c').get('next').get(var.get('RIGHT')) and var.get('c').get('next').get(var.get('RIGHT')).get('connect').get(var.get('UP')).neg())):
                        if ((var.get('c').get('next').get(var.get('DOWN')) and var.get('c').get('next').get(var.get('DOWN')).get('connect').get(var.get('RIGHT'))) and var.get('c').get('next').get(var.get('DOWN')).get('next').get(var.get('RIGHT')).get('connect').get(var.get('RIGHT'))).neg():
                            var.get('c').put('isJoinCandidate', Js(True))
                            if (var.get('Math').callprop('random')<=Js(0.25)):
                                var.get('c').get('connect').put(var.get('UP'), Js(True))
            finally:
                    (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        #for JS loop
        var.put('x', Js(0.0))
        while (var.get('x')<var.get('cols')):
            try:
                var.put('c', var.get('cells').get((var.get('x')+((var.get('rows')-Js(1.0))*var.get('cols')))))
                if (((var.get('c').get('connect').get(var.get('LEFT')).neg() and var.get('c').get('connect').get(var.get('RIGHT')).neg()) and var.get('c').get('connect').get(var.get('DOWN')).neg()) and (var.get('c').get('connect').get(var.get('UP')).neg() or var.get('c').get('next').get(var.get('UP')).get('connect').get(var.get('UP')).neg())):
                    if ((var.get('c').get('next').get(var.get('LEFT')).neg() or var.get('c').get('next').get(var.get('LEFT')).get('connect').get(var.get('DOWN')).neg()) and (var.get('c').get('next').get(var.get('RIGHT')) and var.get('c').get('next').get(var.get('RIGHT')).get('connect').get(var.get('DOWN')).neg())):
                        if ((var.get('c').get('next').get(var.get('UP')) and var.get('c').get('next').get(var.get('UP')).get('connect').get(var.get('RIGHT'))) and var.get('c').get('next').get(var.get('UP')).get('next').get(var.get('RIGHT')).get('connect').get(var.get('RIGHT'))).neg():
                            var.get('c').put('isJoinCandidate', Js(True))
                            if (var.get('Math').callprop('random')<=Js(0.25)):
                                var.get('c').get('connect').put(var.get('DOWN'), Js(True))
            finally:
                    (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        pass
        #for JS loop
        var.put('y', Js(1.0))
        while (var.get('y')<(var.get('rows')-Js(1.0))):
            try:
                var.put('c', var.get('cells').get(((var.get('cols')-Js(1.0))+(var.get('y')*var.get('cols')))))
                if var.get('c').get('raiseHeight'):
                    continue
                if ((((var.get('c').get('connect').get(var.get('RIGHT')).neg() and var.get('c').get('connect').get(var.get('UP')).neg()) and var.get('c').get('connect').get(var.get('DOWN')).neg()) and var.get('c').get('next').get(var.get('UP')).get('connect').get(var.get('RIGHT')).neg()) and var.get('c').get('next').get(var.get('DOWN')).get('connect').get(var.get('RIGHT')).neg()):
                    if var.get('c').get('connect').get(var.get('LEFT')):
                        var.put('c2', var.get('c').get('next').get(var.get('LEFT')))
                        if ((var.get('c2').get('connect').get(var.get('UP')).neg() and var.get('c2').get('connect').get(var.get('DOWN')).neg()) and var.get('c2').get('connect').get(var.get('LEFT')).neg()):
                            var.get('c').put('isJoinCandidate', Js(True))
                            if (var.get('Math').callprop('random')<=Js(0.5)):
                                var.get('c').get('connect').put(var.get('RIGHT'), Js(True))
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    PyJs_anonymous_41_._set_name('anonymous')
    var.put('joinWalls', PyJs_anonymous_41_)
    var.put('genCount', Js(0.0))
    while Js(True):
        var.get('reset')()
        var.get('gen')()
        (var.put('genCount',Js(var.get('genCount').to_number())+Js(1))-Js(1))
        if var.get('isDesirable')().neg():
            continue
        var.get('setUpScaleCoords')()
        var.get('joinWalls')()
        if var.get('createTunnels')().neg():
            continue
        break
PyJs_anonymous_20_._set_name('anonymous')
var.put('genRandom', PyJs_anonymous_20_)
@Js
def PyJs_anonymous_42_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['tiles', 'x', 'getTileCell', 'tileCells', 'range', 'cl', 'eraseUntilIntersection', 'subrows', 'y0', 'h', 'midcols', 'y', 'setTile', 'i', 'j', 'getTile', 'x0', 'fullcols', 'cu', 'subcols', 'w', 'setTileCell', 'getBotEnergizerRange', 'c', 'getTopEnergizerRange'])
    var.put('tiles', Js([]))
    var.put('tileCells', Js([]))
    var.put('subrows', (((var.get('rows')*Js(3.0))+Js(1.0))+Js(3.0)))
    var.put('subcols', (((var.get('cols')*Js(3.0))-Js(1.0))+Js(2.0)))
    var.put('midcols', (var.get('subcols')-Js(2.0)))
    var.put('fullcols', ((var.get('subcols')-Js(2.0))*Js(2.0)))
    @Js
    def PyJs_anonymous_43_(x, y, v, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'v':v, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'v', 'y'])
        if ((((var.get('x')<Js(0.0)) or (var.get('x')>(var.get('subcols')-Js(1.0)))) or (var.get('y')<Js(0.0))) or (var.get('y')>(var.get('subrows')-Js(1.0)))):
            return var.get('undefined')
        var.put('x', Js(2.0), '-')
        var.get('tiles').put(((var.get('midcols')+var.get('x'))+(var.get('y')*var.get('fullcols'))), var.get('v'))
        var.get('tiles').put((((var.get('midcols')-Js(1.0))-var.get('x'))+(var.get('y')*var.get('fullcols'))), var.get('v'))
    PyJs_anonymous_43_._set_name('anonymous')
    var.put('setTile', PyJs_anonymous_43_)
    @Js
    def PyJs_anonymous_44_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'y'])
        if ((((var.get('x')<Js(0.0)) or (var.get('x')>(var.get('subcols')-Js(1.0)))) or (var.get('y')<Js(0.0))) or (var.get('y')>(var.get('subrows')-Js(1.0)))):
            return var.get('undefined')
        var.put('x', Js(2.0), '-')
        return var.get('tiles').get(((var.get('midcols')+var.get('x'))+(var.get('y')*var.get('fullcols'))))
    PyJs_anonymous_44_._set_name('anonymous')
    var.put('getTile', PyJs_anonymous_44_)
    @Js
    def PyJs_anonymous_45_(x, y, cell, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'cell':cell, 'this':this, 'arguments':arguments}, var)
        var.registers(['cell', 'x', 'y'])
        if ((((var.get('x')<Js(0.0)) or (var.get('x')>(var.get('subcols')-Js(1.0)))) or (var.get('y')<Js(0.0))) or (var.get('y')>(var.get('subrows')-Js(1.0)))):
            return var.get('undefined')
        var.put('x', Js(2.0), '-')
        var.get('tileCells').put((var.get('x')+(var.get('y')*var.get('subcols'))), var.get('cell'))
    PyJs_anonymous_45_._set_name('anonymous')
    var.put('setTileCell', PyJs_anonymous_45_)
    @Js
    def PyJs_anonymous_46_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'y'])
        if ((((var.get('x')<Js(0.0)) or (var.get('x')>(var.get('subcols')-Js(1.0)))) or (var.get('y')<Js(0.0))) or (var.get('y')>(var.get('subrows')-Js(1.0)))):
            return var.get('undefined')
        var.put('x', Js(2.0), '-')
        return var.get('tileCells').get((var.get('x')+(var.get('y')*var.get('subcols'))))
    PyJs_anonymous_46_._set_name('anonymous')
    var.put('getTileCell', PyJs_anonymous_46_)
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('subrows')*var.get('fullcols'))):
        try:
            var.get('tiles').callprop('push', Js('_'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('subrows')*var.get('subcols'))):
        try:
            var.get('tileCells').callprop('push', var.get('undefined'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    pass
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('rows')*var.get('cols'))):
        try:
            var.put('c', var.get('cells').get(var.get('i')))
            #for JS loop
            var.put('x0', Js(0.0))
            while (var.get('x0')<var.get('c').get('final_w')):
                try:
                    #for JS loop
                    var.put('y0', Js(0.0))
                    while (var.get('y0')<var.get('c').get('final_h')):
                        try:
                            var.get('setTileCell')((var.get('c').get('final_x')+var.get('x0')), ((var.get('c').get('final_y')+Js(1.0))+var.get('y0')), var.get('c'))
                        finally:
                                (var.put('y0',Js(var.get('y0').to_number())+Js(1))-Js(1))
                finally:
                        (var.put('x0',Js(var.get('x0').to_number())+Js(1))-Js(1))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    pass
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get('subrows')):
        try:
            #for JS loop
            var.put('x', Js(0.0))
            while (var.get('x')<var.get('subcols')):
                try:
                    var.put('c', var.get('getTileCell')(var.get('x'), var.get('y')))
                    var.put('cl', var.get('getTileCell')((var.get('x')-Js(1.0)), var.get('y')))
                    var.put('cu', var.get('getTileCell')(var.get('x'), (var.get('y')-Js(1.0))))
                    if var.get('c'):
                        if (((var.get('cl') and (var.get('c').get('group')!=var.get('cl').get('group'))) or (var.get('cu') and (var.get('c').get('group')!=var.get('cu').get('group')))) or (var.get('cu').neg() and var.get('c').get('connect').get(var.get('UP')).neg())):
                            var.get('setTile')(var.get('x'), var.get('y'), Js('.'))
                    else:
                        if ((var.get('cl') and (var.get('cl').get('connect').get(var.get('RIGHT')).neg() or (var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')))) or (var.get('cu') and (var.get('cu').get('connect').get(var.get('DOWN')).neg() or (var.get('getTile')(var.get('x'), (var.get('y')-Js(1.0)))==Js('.'))))):
                            var.get('setTile')(var.get('x'), var.get('y'), Js('.'))
                    if (((var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')) and (var.get('getTile')(var.get('x'), (var.get('y')-Js(1.0)))==Js('.'))) and (var.get('getTile')((var.get('x')-Js(1.0)), (var.get('y')-Js(1.0)))==Js('_'))):
                        var.get('setTile')(var.get('x'), var.get('y'), Js('.'))
                finally:
                        (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    pass
    #for JS loop
    var.put('c', var.get('cells').get((var.get('cols')-Js(1.0))))
    while var.get('c'):
        try:
            if var.get('c').get('topTunnel'):
                var.put('y', (var.get('c').get('final_y')+Js(1.0)))
                var.get('setTile')((var.get('subcols')-Js(1.0)), var.get('y'), Js('.'))
                var.get('setTile')((var.get('subcols')-Js(2.0)), var.get('y'), Js('.'))
        finally:
                var.put('c', var.get('c').get('next').get(var.get('DOWN')))
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get('subrows')):
        try:
            #for JS loop
            var.put('x', Js(0.0))
            while (var.get('x')<var.get('subcols')):
                try:
                    def PyJs_LONG_47_(var=var):
                        return ((((((var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')) or (var.get('getTile')(var.get('x'), (var.get('y')-Js(1.0)))==Js('.'))) or (var.get('getTile')((var.get('x')+Js(1.0)), var.get('y'))==Js('.'))) or (var.get('getTile')(var.get('x'), (var.get('y')+Js(1.0)))==Js('.'))) or (var.get('getTile')((var.get('x')-Js(1.0)), (var.get('y')-Js(1.0)))==Js('.'))) or (var.get('getTile')((var.get('x')+Js(1.0)), (var.get('y')-Js(1.0)))==Js('.')))
                    if ((var.get('getTile')(var.get('x'), var.get('y'))!=Js('.')) and ((PyJs_LONG_47_() or (var.get('getTile')((var.get('x')+Js(1.0)), (var.get('y')+Js(1.0)))==Js('.'))) or (var.get('getTile')((var.get('x')-Js(1.0)), (var.get('y')+Js(1.0)))==Js('.')))):
                        var.get('setTile')(var.get('x'), var.get('y'), Js('|'))
                finally:
                        (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    var.get('setTile')(Js(2.0), Js(12.0), Js('-'))
    @Js
    def PyJs_anonymous_48_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['maxy', 'y', 'x', 'miny'])
        pass
        var.put('maxy', (var.get('subrows')/Js(2.0)))
        var.put('x', (var.get('subcols')-Js(2.0)))
        pass
        #for JS loop
        var.put('y', Js(2.0))
        while (var.get('y')<var.get('maxy')):
            try:
                if ((var.get('getTile')(var.get('x'), var.get('y'))==Js('.')) and (var.get('getTile')(var.get('x'), (var.get('y')+Js(1.0)))==Js('.'))):
                    var.put('miny', (var.get('y')+Js(1.0)))
                    break
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        var.put('maxy', var.get('Math').callprop('min', var.get('maxy'), (var.get('miny')+Js(7.0))))
        #for JS loop
        var.put('y', (var.get('miny')+Js(1.0)))
        while (var.get('y')<var.get('maxy')):
            try:
                if (var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')):
                    var.put('maxy', (var.get('y')-Js(1.0)))
                    break
            finally:
                    (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
        return Js({'miny':var.get('miny'),'maxy':var.get('maxy')})
    PyJs_anonymous_48_._set_name('anonymous')
    var.put('getTopEnergizerRange', PyJs_anonymous_48_)
    @Js
    def PyJs_anonymous_49_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['maxy', 'y', 'x', 'miny'])
        var.put('miny', (var.get('subrows')/Js(2.0)))
        pass
        var.put('x', (var.get('subcols')-Js(2.0)))
        pass
        #for JS loop
        var.put('y', (var.get('subrows')-Js(3.0)))
        while (var.get('y')>=var.get('miny')):
            try:
                if ((var.get('getTile')(var.get('x'), var.get('y'))==Js('.')) and (var.get('getTile')(var.get('x'), (var.get('y')+Js(1.0)))==Js('.'))):
                    var.put('maxy', var.get('y'))
                    break
            finally:
                    (var.put('y',Js(var.get('y').to_number())-Js(1))+Js(1))
        var.put('miny', var.get('Math').callprop('max', var.get('miny'), (var.get('maxy')-Js(7.0))))
        #for JS loop
        var.put('y', (var.get('maxy')-Js(1.0)))
        while (var.get('y')>var.get('miny')):
            try:
                if (var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')):
                    var.put('miny', (var.get('y')+Js(1.0)))
                    break
            finally:
                    (var.put('y',Js(var.get('y').to_number())-Js(1))+Js(1))
        return Js({'miny':var.get('miny'),'maxy':var.get('maxy')})
    PyJs_anonymous_49_._set_name('anonymous')
    var.put('getBotEnergizerRange', PyJs_anonymous_49_)
    var.put('x', (var.get('subcols')-Js(2.0)))
    pass
    pass
    if var.put('range', var.get('getTopEnergizerRange')()):
        var.put('y', var.get('getRandomInt')(var.get('range').get('miny'), var.get('range').get('maxy')))
        var.get('setTile')(var.get('x'), var.get('y'), Js('o'))
    if var.put('range', var.get('getBotEnergizerRange')()):
        var.put('y', var.get('getRandomInt')(var.get('range').get('miny'), var.get('range').get('maxy')))
        var.get('setTile')(var.get('x'), var.get('y'), Js('o'))
    @Js
    def PyJs_anonymous_50_(x, y, this, arguments, var=var):
        var = Scope({'x':x, 'y':y, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 'adj', 'y'])
        pass
        while Js(True):
            var.put('adj', Js([]))
            if (var.get('getTile')((var.get('x')-Js(1.0)), var.get('y'))==Js('.')):
                var.get('adj').callprop('push', Js({'x':(var.get('x')-Js(1.0)),'y':var.get('y')}))
            if (var.get('getTile')((var.get('x')+Js(1.0)), var.get('y'))==Js('.')):
                var.get('adj').callprop('push', Js({'x':(var.get('x')+Js(1.0)),'y':var.get('y')}))
            if (var.get('getTile')(var.get('x'), (var.get('y')-Js(1.0)))==Js('.')):
                var.get('adj').callprop('push', Js({'x':var.get('x'),'y':(var.get('y')-Js(1.0))}))
            if (var.get('getTile')(var.get('x'), (var.get('y')+Js(1.0)))==Js('.')):
                var.get('adj').callprop('push', Js({'x':var.get('x'),'y':(var.get('y')+Js(1.0))}))
            if (var.get('adj').get('length')==Js(1.0)):
                var.get('setTile')(var.get('x'), var.get('y'), Js(' '))
                var.put('x', var.get('adj').get('0').get('x'))
                var.put('y', var.get('adj').get('0').get('y'))
            else:
                break
    PyJs_anonymous_50_._set_name('anonymous')
    var.put('eraseUntilIntersection', PyJs_anonymous_50_)
    var.put('x', (var.get('subcols')-Js(1.0)))
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<var.get('subrows')):
        try:
            if (var.get('getTile')(var.get('x'), var.get('y'))==Js('.')):
                var.get('eraseUntilIntersection')(var.get('x'), var.get('y'))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    var.get('setTile')(Js(1.0), (var.get('subrows')-Js(8.0)), Js(' '))
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<Js(7.0)):
        try:
            var.put('y', (var.get('subrows')-Js(14.0)))
            var.get('setTile')(var.get('i'), var.get('y'), Js(' '))
            var.put('j', Js(1.0))
            while (((var.get('getTile')(var.get('i'), (var.get('y')+var.get('j')))==Js('.')) and (var.get('getTile')((var.get('i')-Js(1.0)), (var.get('y')+var.get('j')))==Js('|'))) and (var.get('getTile')((var.get('i')+Js(1.0)), (var.get('y')+var.get('j')))==Js('|'))):
                var.get('setTile')(var.get('i'), (var.get('y')+var.get('j')), Js(' '))
                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
            var.put('y', (var.get('subrows')-Js(20.0)))
            var.get('setTile')(var.get('i'), var.get('y'), Js(' '))
            var.put('j', Js(1.0))
            while (((var.get('getTile')(var.get('i'), (var.get('y')-var.get('j')))==Js('.')) and (var.get('getTile')((var.get('i')-Js(1.0)), (var.get('y')-var.get('j')))==Js('|'))) and (var.get('getTile')((var.get('i')+Js(1.0)), (var.get('y')-var.get('j')))==Js('|'))):
                var.get('setTile')(var.get('i'), (var.get('y')-var.get('j')), Js(' '))
                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<Js(7.0)):
        try:
            var.put('x', Js(6.0))
            var.put('y', ((var.get('subrows')-Js(14.0))-var.get('i')))
            var.get('setTile')(var.get('x'), var.get('y'), Js(' '))
            var.put('j', Js(1.0))
            while (((var.get('getTile')((var.get('x')+var.get('j')), var.get('y'))==Js('.')) and (var.get('getTile')((var.get('x')+var.get('j')), (var.get('y')-Js(1.0)))==Js('|'))) and (var.get('getTile')((var.get('x')+var.get('j')), (var.get('y')+Js(1.0)))==Js('|'))):
                var.get('setTile')((var.get('x')+var.get('j')), var.get('y'), Js(' '))
                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return (((((Js('____________________________')+Js('____________________________'))+Js('____________________________'))+var.get('tiles').callprop('join', Js('')))+Js('____________________________'))+Js('____________________________'))
PyJs_anonymous_42_._set_name('anonymous')
var.put('getTiles', PyJs_anonymous_42_)
@Js
def PyJs_anonymous_51_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return (Js('#')+(Js('00000')+((var.get('Math').callprop('random')*(Js(1.0)<<Js(24.0)))|Js(0.0)).callprop('toString', Js(16.0))).callprop('slice', (-Js(6.0))))
PyJs_anonymous_51_._set_name('anonymous')
var.put('randomColor', PyJs_anonymous_51_)
@Js
def PyJs_anonymous_52_(ctx, left, top, size, title, options, this, arguments, var=var):
    var = Scope({'ctx':ctx, 'left':left, 'top':top, 'size':size, 'title':title, 'options':options, 'this':this, 'arguments':arguments}, var)
    var.registers(['arrowsize', 'top', 'ctx', 'options', 'x', 'title', 'y', 'c', 'i', 'size', 'left'])
    var.get('ctx').callprop('save')
    var.get('ctx').callprop('translate', var.get('left'), var.get('top'))
    var.get('ctx').put('font', ((Js('bold ')+(var.get('size')/Js(3.0)))+Js('px sans-serif')))
    var.get('ctx').put('textBaseline', Js('bottom'))
    var.get('ctx').put('textAlign', Js('left'))
    var.get('ctx').put('fillStyle', Js('#000'))
    var.get('ctx').callprop('fillText', var.get('title'), Js(0.0), (-Js(5.0)))
    var.get('ctx').callprop('beginPath')
    #for JS loop
    var.put('y', Js(0.0))
    while (var.get('y')<=var.get('rows')):
        try:
            var.get('ctx').callprop('moveTo', Js(0.0), (var.get('y')*var.get('size')))
            var.get('ctx').callprop('lineTo', (var.get('cols')*var.get('size')), (var.get('y')*var.get('size')))
        finally:
                (var.put('y',Js(var.get('y').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('x', Js(0.0))
    while (var.get('x')<=var.get('cols')):
        try:
            var.get('ctx').callprop('moveTo', (var.get('x')*var.get('size')), Js(0.0))
            var.get('ctx').callprop('lineTo', (var.get('x')*var.get('size')), (var.get('rows')*var.get('size')))
        finally:
                (var.put('x',Js(var.get('x').to_number())+Js(1))-Js(1))
    var.get('ctx').put('lineWidth', Js('1'))
    var.get('ctx').put('strokeStyle', Js('rgba(0,0,0,0.2)'))
    var.get('ctx').callprop('stroke')
    var.get('ctx').put('font', ((var.get('size')/Js(3.0))+Js('px sans-serif')))
    var.get('ctx').put('textBaseline', Js('middle'))
    var.get('ctx').put('textAlign', Js('center'))
    var.put('arrowsize', (var.get('size')/Js(6.0)))
    var.get('ctx').put('lineWidth', Js('3'))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('cols')*var.get('rows'))):
        try:
            var.put('c', var.get('cells').get(var.get('i')))
            var.put('x', (var.get('i')%var.get('cols')))
            var.put('y', var.get('Math').callprop('floor', (var.get('i')/var.get('cols'))))
            if (var.get('options').get('drawRaiseHeightCandidate') and var.get('c').get('isRaiseHeightCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(0,0,255,0.2)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawShrinkWidthCandidate') and var.get('c').get('isShrinkWidthCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(255,0,0,0.2)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawJoinCandidate') and var.get('c').get('isJoinCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(0,255,0,0.2)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawSingleDeadEnd') and var.get('c').get('isSingleDeadEndCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(255,255,0,0.4)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawDoubleDeadEnd') and var.get('c').get('isDoubleDeadEndCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(0,255,255,0.2)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawVoidTunnel') and var.get('c').get('isVoidTunnelCandidate')):
                var.get('ctx').put('fillStyle', Js('rgba(0,0,0,0.2)'))
                var.get('ctx').callprop('fillRect', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')), var.get('size'), var.get('size'))
            if (var.get('options').get('drawChosenTunnel') and var.get('c').get('topTunnel')):
                var.get('ctx').callprop('beginPath')
                var.get('ctx').callprop('save')
                var.get('ctx').callprop('translate', ((var.get('x')*var.get('size'))+(var.get('size')/Js(2.0))), ((var.get('y')*var.get('size'))+Js(5.0)))
                var.get('ctx').callprop('moveTo', (-var.get('arrowsize')), var.get('arrowsize'))
                var.get('ctx').callprop('lineTo', Js(0.0), Js(0.0))
                var.get('ctx').callprop('lineTo', var.get('arrowsize'), var.get('arrowsize'))
                var.get('ctx').put('strokeStyle', Js('rgba(0,255,0,0.7)'))
                var.get('ctx').callprop('stroke')
                var.get('ctx').callprop('restore')
            else:
                if (var.get('options').get('drawEdgeTunnel') and var.get('c').get('isEdgeTunnelCandidate')):
                    var.get('ctx').callprop('beginPath')
                    var.get('ctx').callprop('save')
                    var.get('ctx').callprop('translate', ((var.get('x')*var.get('size'))+(var.get('size')/Js(2.0))), ((var.get('y')*var.get('size'))+Js(5.0)))
                    var.get('ctx').callprop('moveTo', (-var.get('arrowsize')), var.get('arrowsize'))
                    var.get('ctx').callprop('lineTo', Js(0.0), Js(0.0))
                    var.get('ctx').callprop('lineTo', var.get('arrowsize'), var.get('arrowsize'))
                    var.get('ctx').put('strokeStyle', Js('rgba(0,0,0,0.7)'))
                    var.get('ctx').callprop('stroke')
                    var.get('ctx').callprop('restore')
            if (var.get('options').get('drawRaiseHeight') and var.get('c').get('raiseHeight')):
                var.get('ctx').callprop('beginPath')
                var.get('ctx').callprop('save')
                var.get('ctx').callprop('translate', ((var.get('x')*var.get('size'))+(var.get('size')/Js(2.0))), (((var.get('y')*var.get('size'))+var.get('size'))-var.get('arrowsize')))
                var.get('ctx').callprop('moveTo', (-var.get('arrowsize')), (-var.get('arrowsize')))
                var.get('ctx').callprop('lineTo', Js(0.0), Js(0.0))
                var.get('ctx').callprop('lineTo', var.get('arrowsize'), (-var.get('arrowsize')))
                var.get('ctx').put('strokeStyle', Js('rgba(0,0,255,0.7)'))
                var.get('ctx').callprop('stroke')
                var.get('ctx').callprop('restore')
            if (var.get('options').get('drawShrinkWidth') and var.get('c').get('shrinkWidth')):
                var.get('ctx').callprop('beginPath')
                var.get('ctx').callprop('save')
                var.get('ctx').callprop('translate', ((((var.get('x')*var.get('size'))+var.get('size'))-var.get('arrowsize'))-var.get('arrowsize')), ((var.get('y')*var.get('size'))+(var.get('size')/Js(2.0))))
                var.get('ctx').callprop('moveTo', var.get('arrowsize'), (-var.get('arrowsize')))
                var.get('ctx').callprop('lineTo', Js(0.0), Js(0.0))
                var.get('ctx').callprop('lineTo', var.get('arrowsize'), var.get('arrowsize'))
                var.get('ctx').callprop('restore')
                var.get('ctx').put('strokeStyle', Js('rgba(255,0,0,0.7)'))
                var.get('ctx').callprop('stroke')
            if (var.get('options').get('drawNumbers') and (var.get('c').get('no')!=var.get('undefined'))):
                var.get('ctx').put('fillStyle', Js('#000'))
                var.get('ctx').callprop('fillText', var.get('c').get('no'), ((var.get('x')*var.get('size'))+(var.get('size')/Js(2.0))), ((var.get('y')*var.get('size'))+(var.get('size')/Js(2.0))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('ctx').callprop('beginPath')
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('cols')*var.get('rows'))):
        try:
            var.put('c', var.get('cells').get(var.get('i')))
            var.put('x', (var.get('i')%var.get('cols')))
            var.put('y', var.get('Math').callprop('floor', (var.get('i')/var.get('cols'))))
            if var.get('c').get('connect').get(var.get('UP')).neg():
                var.get('ctx').callprop('moveTo', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')))
                var.get('ctx').callprop('lineTo', ((var.get('x')*var.get('size'))+var.get('size')), (var.get('y')*var.get('size')))
            if var.get('c').get('connect').get(var.get('DOWN')).neg():
                var.get('ctx').callprop('moveTo', (var.get('x')*var.get('size')), ((var.get('y')*var.get('size'))+var.get('size')))
                var.get('ctx').callprop('lineTo', ((var.get('x')*var.get('size'))+var.get('size')), ((var.get('y')*var.get('size'))+var.get('size')))
            if var.get('c').get('connect').get(var.get('LEFT')).neg():
                var.get('ctx').callprop('moveTo', (var.get('x')*var.get('size')), (var.get('y')*var.get('size')))
                var.get('ctx').callprop('lineTo', (var.get('x')*var.get('size')), ((var.get('y')*var.get('size'))+var.get('size')))
            if var.get('c').get('connect').get(var.get('RIGHT')).neg():
                var.get('ctx').callprop('moveTo', ((var.get('x')*var.get('size'))+var.get('size')), (var.get('y')*var.get('size')))
                var.get('ctx').callprop('lineTo', ((var.get('x')*var.get('size'))+var.get('size')), ((var.get('y')*var.get('size'))+var.get('size')))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('ctx').put('lineWidth', Js('3'))
    var.get('ctx').put('lineCap', Js('round'))
    var.get('ctx').put('strokeStyle', Js('rgba(0,0,0,0.9)'))
    var.get('ctx').callprop('stroke')
    var.get('ctx').callprop('restore')
PyJs_anonymous_52_._set_name('anonymous')
var.put('drawCells', PyJs_anonymous_52_)
@Js
def PyJs_anonymous_53_(ctx, left, top, size, this, arguments, var=var):
    var = Scope({'ctx':ctx, 'left':left, 'top':top, 'size':size, 'this':this, 'arguments':arguments}, var)
    var.registers(['subcols', 'subrows', 'top', 'ctx', 'tiles', 'fullcols', 'color', 'x', 'y', 'subsize', 'i', 'size', 'left'])
    var.get('ctx').callprop('save')
    var.get('ctx').callprop('translate', var.get('left'), var.get('top'))
    var.put('subsize', (var.get('size')/Js(3.0)))
    var.put('subrows', (((var.get('rows')*Js(3.0))+Js(1.0))+Js(3.0)))
    var.put('subcols', (((var.get('cols')*Js(3.0))-Js(1.0))+Js(2.0)))
    var.put('fullcols', ((var.get('subcols')-Js(2.0))*Js(2.0)))
    pass
    pass
    var.get('ctx').callprop('beginPath')
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<=var.get('subrows')):
        try:
            var.put('y', (var.get('i')*var.get('subsize')))
            var.get('ctx').callprop('moveTo', Js(0.0), var.get('y'))
            var.get('ctx').callprop('lineTo', (var.get('fullcols')*var.get('subsize')), var.get('y'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<=var.get('fullcols')):
        try:
            var.put('x', (var.get('i')*var.get('subsize')))
            var.get('ctx').callprop('moveTo', var.get('x'), Js(0.0))
            var.get('ctx').callprop('lineTo', var.get('x'), (var.get('subrows')*var.get('subsize')))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('ctx').put('lineWidth', Js('1'))
    var.get('ctx').put('strokeStyle', Js('rgba(0,0,0,0.3)'))
    var.get('ctx').callprop('stroke')
    var.put('tiles', var.get('getTiles')())
    var.put('fillStyles', Js({'.':Js('rgba(0,0,0,0.4)'),'o':Js('rgba(0,0,0,0.4)'),' ':Js('rgba(0,0,0,0.4)'),'|':Js('rgba(0,0,0,0.1)'),'-':Js('rgba(0,0,0,0.0)'),'_':Js('rgba(0,0,0,0)')}))
    pass
    pass
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<(var.get('subrows')*var.get('fullcols'))):
        try:
            var.put('x', (var.get('i')%var.get('fullcols')))
            var.put('y', var.get('Math').callprop('floor', (var.get('i')/var.get('fullcols'))))
            var.get('ctx').put('fillStyle', (var.get('fillStyles').get(var.get('tiles').get(var.get('i'))) or Js('#F00')))
            var.get('ctx').callprop('fillRect', (var.get('x')*var.get('subsize')), (var.get('y')*var.get('subsize')), var.get('subsize'), var.get('subsize'))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    var.get('ctx').callprop('restore')
PyJs_anonymous_53_._set_name('anonymous')
var.put('drawTiles', PyJs_anonymous_53_)
@Js
def PyJs_anonymous_54_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['map'])
    var.get('genRandom')()
    var.put('map', var.get('Map').create(Js(28.0), Js(36.0), var.get('getTiles')()))
    var.get('map').put('name', Js(''))
    var.get('map').put('wallFillColor', var.get('randomColor')())
    var.get('map').put('wallStrokeColor', var.get('rgbString')(var.get('hslToRgb')(var.get('Math').callprop('random'), var.get('Math').callprop('random'), ((var.get('Math').callprop('random')*Js(0.4))+Js(0.6)))))
    var.get('map').put('pelletColor', Js('#ffb8ae'))
    return var.get('map')
PyJs_anonymous_54_._set_name('anonymous')
var.put('mapgen', PyJs_anonymous_54_)
pass


# Add lib to the module scope
mapgen = var.to_python()