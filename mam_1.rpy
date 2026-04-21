label chapter1_anon_part1:
    # --- 第一章 标题字卡 ---
    scene black with Dissolve(2.0)
    pause 1.0
    
    show text "{size=28}{space=10}Chapter 1{/size}\n\n{size=60}{font=fonts/cinematic.ttf}The Deceitful Shell{/font}{/size}\n\n{size=36}第一部：欺骸篇{/size}" at truecenter with Dissolve(2.5)
    pause 4.0
    hide text with Dissolve(2.0)
    pause 1.0
    
    show text "{size=48}{font=fonts/cinematic.ttf}第一章：千早爱音\n[ 错位的涉谷 ]{/font}{/size}" at truecenter with dissolve
    pause 3.0
    hide text with dissolve
    pause 1.5

    # --- Part 1: 发薪日与温室的默契 ---
    scene bg_school_gate_afternoon with Dissolve(2.0)
    play music "audio/bgm/afternoon_breeze.ogg" fadein 3.0 loop volume 0.5
    
    mc "（第二周。周五的黄昏。）"
    mc "（自从第一天在校园里被那些月之森的大小姐们像看珍稀动物一样围观后，我就学聪明了。）"
    mc "（我调整了打工的时间，每天都等放学铃响过半小时、校园里几乎没人的时候，才偷偷溜进那个废弃的旧第二温室。）"
    
    mc "（毕竟，我只是个拿时薪的底层保洁员。少惹麻烦，闷声赚钱才是王道。）"
    
    scene black with Dissolve(1.5)
    play sound "audio/story/footsteps_gravel.ogg" volume 0.6
    pause 1.5
    play sound "audio/story/rusty_door_open.ogg"
    
    scene bg_greenhouse_inside_dusk with Dissolve(2.0)
    
    mc "（推开那扇沉重的铁门，迎接我的，依然是那股熟悉的腐叶土味。）"
    mc "（以及……那个永远蹲在角落里的背影。）"
    
    show mu1_4 at t11 with dissolve:
        zoom 0.8
        yoffset -80
        
    play sound "audio/story/shovel_digging_slow.ogg" loop volume 0.4
    "沙……沙……"
    
    mc "（那个不可思议的女孩，若叶睦。她依然在那里面无表情地给那株已经完全枯黄死掉的黄瓜苗松土。）"
    mc "（在这个被时间遗忘的玻璃棺材里，我和她形成了一种极其诡异的默契。）"
    mc "（她不说话，我也不搭茬。就像两只共处一室、但互不侵犯领地的流浪猫。）"
    
    stop sound fadeout 2.0
    
    mc "（我照常拿起扫帚清理落叶。直到——口袋里的手机突然震动了一下。）"
    
    play sound "audio/story/phone_vibrate.ogg"
    pause 1.0
    
    mc "（我拿出手机。屏幕上弹出了一条银行的到账通知。）"
    
    show text "{size=30}【账户提醒】您的外包兼职周薪 14,500円 已汇入账户。{/size}" at truecenter with dissolve
    pause 2.5
    hide text with dissolve
    
    mc "（！！！）"
    mc "（发工资了！我看着那一长串数字，这几天腰酸背痛的阴霾瞬间一扫而空。）"
    mc "（Boss DD-8 效果器！只要今天下班冲去涉谷的乐器店，那块我在梦里都在推弦的神器，就是我的了！）"
    
    mc "（激动的心情让我有些忘乎所以。我收拾好工具，走到温室门口。）"
    
    mc "（在推开铁门前，我鬼使神差地停下了脚步，回头看向那个依然背对着我的女孩。）"
    
    mc "那个……我今天发工资了。终于能去买那个心心念念的效果器了。"
    mc "下周见。"
    
    pause 2.0
    
    mc "（……依然是意料之中的沉默。）"
    mc "（我自嘲地笑了笑，觉得自己真是兴奋过头了，居然妄想这块冰山能给点反应。）"
    mc "（我转过身，手握住冰冷的门把手，准备推门离开。）"
    
    mu1 "……"
    
    mc "（嗯？）"
    
    hide mu1_4 with dissolve
    show mu1_3 at t11 with dissolve:
        zoom 0.8
        yoffset -80
        
    mu1 "……路上小心。"
    
    mc "（声音极轻。轻得像是一片快要融化的雪花，几乎被生锈铰链的摩擦声彻底盖住。）"
    mc "（但我真真切切地听到了。）"
    mc "（我愣了一下，看着她依然没有转过来的背影，嘴角忍不住疯狂上扬。）"
    
    mc "（这就算是……微小的破冰吧。）"
    
    mc "嗯！谢谢！"
    
    play sound "audio/story/rusty_door_close.ogg"
    scene black with Dissolve(2.0)
    stop music fadeout 3.0
    
    mc "（我怀揣着难以言喻的轻快心情，踏上了前往涉谷的电车。）"
    mc "（那时的我根本不知道——）"
    mc "（等待我的，将是一场怎样荒诞且惊悚的认知撕裂。）"

label chapter1_anon_part2:
    # --- Part 2: 错位的乐器店 ---
    scene bg_shibuya_street_night with Dissolve(2.5)
    play music "audio/bgm/shibuya_upbeat.ogg" fadein 2.0 loop volume 0.6
    
    mc "（涉谷。这个永远喧嚣、永远被霓虹灯和人潮淹没的十字路口。）"
    mc "（我穿过拥挤的人群，熟练地钻进了街角那家我踩点过无数次的大型乐器店。）"
    
    scene bg_instrument_store with Dissolve(1.5)
    play sound "audio/story/store_bell.ogg"
    pause 1.0
    
    mc "（一进门，混合着木材、金属和空气清新剂的味道扑面而来。这就是天堂的味道啊！）"
    mc "（我直奔效果器专柜，隔着玻璃，死死盯着那块白色的 Boss DD-8 延迟效果器。）"
    
    mc "（这简直就是一件完美的工业艺术品。我甚至已经在脑海里听到了它插上电后，那种空灵又充满颗粒感的回声。）"
    
    mc "（我拿出手机，正准备打开计算机，精打细算一下加上税和各类满减优惠券后的最终价格……）"
    
    # 悬念引爆点
    stop music
    play sound "audio/story/surprised_gasp.ogg"
    
    voice "audio/yuyin/anon_surprise.ogg"
    "？？？" "……诶？！"
    
    mc "（一个充满元气、但此刻却因为极度错愕而破音的女声，突然在我身后的不远处炸响。）"
    
    voice "audio/yuyin/anon_mutsumi.ogg"
    "粉发少女" "睦、睦酱？！你怎么会在这里？！"
    
    play sound "audio/story/heartbeat_single.ogg" volume 0.8
    with vpunch
    
    mc "（睦？）"
    mc "（我的心脏猛地漏跳了一拍。）"
    mc "（有人……认识那个温室大小姐？而且她现在也在这家店里？）"