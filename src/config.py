#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Dict, Any
import json
import os
from PySide6.QtGui import QColor


def _user_data_dir() -> str:
    """Return the per-user data directory: %APPDATA%\\TinyType on Windows."""
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    return os.path.join(base, "TinyType")


class Config:
    """Manages application configuration and settings persistence."""

    def __init__(self, config_path: str = "") -> None:
        """
        Initialize configuration manager.

        Args:
            config_path: Path to configuration file. Defaults to %APPDATA%\\TinyType\\config.json.
        """
        if not config_path:
            config_path = os.path.join(_user_data_dir(), "config.json")
        self.config_path: str = config_path
        self._migrate_legacy()
        self.settings: Dict[str, Any] = self._load_defaults()
        self.load()

    def _migrate_legacy(self) -> None:
        """Copy config from the old data/ directory if the new location is empty."""
        if os.path.exists(self.config_path):
            return
        legacy = os.path.join("data", "config.json")
        if os.path.exists(legacy):
            import shutil
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            shutil.copy2(legacy, self.config_path)
    
    def _load_defaults(self) -> Dict[str, Any]:
        """
        Load default configuration settings.
        
        Returns:
            Dictionary of default settings
        """
        return {
            "font_family": "Courier New",
            "font_size": 8,
            "untyped_color": "#ffffff",
            "typed_color": "#808080",
            "error_color": "#FF0000",
            "window_color": "#000000",
            "bg_opacity": 128,
            "move_per_word": False,
            "text_align": "left",
            "pause_on_focus": False,
            "position": "center",
            "typing_width": 500,
            "typing_height": 60,
            "show_border": False,
            "active_test": 0,
            "use_random": False,
            "typing_tests": [
                {"name": "Default", "text": ""},
                {"name": "5k English", "text": "the of and a in for is on that by this with I you it not or be are from at as your all have new more an was we will home can about if page has search free but our one other do no information time they site he up may what which their news out use any there see only so his when contact here business who web also now help get view online first am been would how were me services some these click its like service than find price date back top people had list name just over state year day into email two health world next used go work last most products music buy data make them should product system post her city add policy number such please available copyright support message after best software then good video well where info rights public books high school through each links she review years order very privacy book items company read group need many user said does set under general research university January mail full map reviews program life know games way days management part could great united hotel real item international center must store travel comments made development report off member details line terms before hotels did send right type because local those using results office education national car design take posted internet address community within states area want phone shipping reserved subject between forum family long based code show even black check special prices website index being women much sign file link open today technology south case project same pages version section own found sports house related security both county American photo game members power while care network down computer systems three total place end following download him without per access think north resources current posts big media law control water history pictures size art personal since including guide shop directory board location change white text small rating rate government children during return students shopping account times sites level digital profile previous form events love old main call hours image department title description insurance another why shall property class still money quality every listing content country private little visit save tools low reply customer December compare movies include college value article man card jobs provide food source author different press learn sale around print course job Canada process teen room stock training too credit point join science men categories advanced west sales look English left team estate box conditions select windows photos gay thread week category note live large gallery table register however June October November market library really action start series model features air industry plan human provided yes required second hot accessories cost movie forums march September better say questions July going medical test friend come server study application cart staff articles feedback again play looking issues April never users complete street topic comment financial things working against standard tax person below mobile less got blog party payment equipment login student let programs offers legal above recent park stores side act problem red give memory performance social August quote language story sell options experience rates create key body young America important field few east paper single age activities club example girls additional password latest something road gift question changes night hard Texas pay four poker status browse issue range building seller court February always result audio light write offer blue groups easy given files event release analysis request fax China making picture needs possible might professional yet month major star areas future space committee hand sun cards problems London Washington meeting become interest child keep enter California share similar garden schools million added reference companies listed baby learning energy run delivery net popular term film stories put computers journal reports try welcome central images president notice god original head radio until cell color self council away includes track Australia discussion archive once others entertainment agreement format least society months log safety friends sure trade edition cars messages marketing tell further updated association able having provides fun already green studies close common drive specific several gold living collection called short arts lot ask display limited powered solutions means director daily beach past natural whether due electronics five upon period planning database says official weather mar land average done technical window France pro region island record direct microsoft conference environment records district calendar costs style front statement update parts ever downloads early miles sound resource present applications either ago document word works material bill written talk federal hosting rules final adult tickets thing requirements via cheap kids finance true minutes else mark third rock gifts Europe reading topics bad individual tips plus auto cover usually edit together videos percent fast function fact unit getting global tech meet far economic player projects lyrics often subscribe submit Germany amount watch included feel though bank risk thanks everything deals various words production commercial weight town heart advertising received choose treatment newsletter archives points knowledge magazine error camera girl currently construction toys registered clear golf receive domain methods chapter makes protection policies loan wide beauty manager India position taken sort listings models known half cases step engineering Florida simple quick none wireless license Friday lake whole annual published later basic shows corporate church method purchase customers active response practice hardware figure materials fire holiday chat enough designed along among death writing speed countries loss face brand discount higher effects created remember standards oil bit yellow political increase advertise kingdom base near environmental thought stuff French storage Japan doing loans shoes entry stay nature orders availability Africa summary turn mean growth notes agency king Monday European activity copy although drug pics western income force cash employment overall bay river commission ad package contents seen players engine port album regional stop supplies started administration bar institute views plans double dog build screen exchange types soon sponsored lines electronic continue across benefits needed season apply someone held anything printer condition effective believe organization effect asked mind Sunday selection casino lost tour menu volume cross anyone mortgage hope silver corporation wish inside solution mature role rather weeks addition came supply nothing certain executive running lower necessary union jewelry according clothing particular fine names homepage hour gas skills six bush islands advice career military rental decision leave British teens huge sat woman facilities zip bid kind sellers middle move cable opportunities taking values division coming Tuesday object appropriate machine logo length actually nice score statistics client returns capital follow sample investment sent shown saturday Christmas England culture band flash lead choice went starting registration Thursday courses consumer hi airport foreign artist outside furniture levels channel letter mode phones ideas Wednesday structure fund summer allow degree contract button releases wed homes super male matter custom Virginia almost took located multiple Asian distribution editor inn industrial cause potential song focus late fall featured idea rooms female responsible communications win associated primary cancer numbers reason tool browser spring foundation answer voice friendly schedule documents communication purpose feature bed comes police everyone independent approach cameras brown physical operating hill maps medicine deal hold ratings Chicago forms glass happy smith wanted developed thank safe unique survey prior telephone sport ready feed animal sources Mexico population regular secure navigation operations therefore simply evidence station christian round favorite understand option master valley recently probably rentals sea built publications blood cut worldwide improve connection publisher hall larger networks earth parents impact transfer introduction kitchen strong wedding properties hospital ground overview ship accommodation owners disease excellent paid Italy perfect hair opportunity kit classic basis command cities express award distance tree assessment ensure thus wall involved extra especially interface partners budget rated guides success maximum operation existing quite selected boy patients restaurants beautiful warning wine locations horse vote forward flowers stars significant lists technologies owner retail animals useful directly manufacturer ways son providing rule housing takes bring catalog trying mother authority considered told traffic joined input strategy feet agent valid bin modern senior Ireland teaching door grand testing trial charge units instead Canadian cool normal wrote enterprise ships entire educational leading metal positive fitness Chinese opinion Asia football abstract uses output funds greater likely develop employees artists alternative processing responsibility resolution guest seems publication pass relations trust van contains session multi photography republic fees components vacation century academic assistance completed skin graphics Indian ads expected ring grade dating Pacific mountain organizations pop filter mailing vehicle longer consider northern behind panel floor German buying match proposed default require Iraq boys outdoor deep morning otherwise allows rest protein plant reported hit transportation pool politics partner disclaimer authors boards faculty parties fish membership mission eye string sense modified pack released stage internal goods recommended born unless detailed Japanese race approved background target except character maintenance ability maybe functions moving brands places pretty trademarks Spain southern yourself winter battery youth pressure submitted Boston debt keywords medium television interested core break purposes throughout sets dance wood itself defined papers playing awards fee studio reader virtual device established answers rent remote dark programming external apple regarding instructions offered theory enjoy remove aid surface minimum visual host variety teachers manual block subjects agents increased repair fair civil steel understanding songs fixed wrong beginning hands associates finally updates desktop classes Paris Ohio gets sector capacity requires jersey fat fully father electric saw instruments quotes officer driver businesses dead respect unknown specified restaurant trip worth procedures poor teacher eyes relationship workers farm peace traditional campus showing creative coast benefit progress funding devices lord grant agree fiction hear sometimes watches careers beyond goes families led museum themselves fan transport interesting blogs wife evaluation accepted former implementation ten hits zone complex cat galleries references die presented flat flow agencies literature respective parent Spanish Michigan Columbia setting scale stand economy highest helpful monthly critical frame musical definition secretary networking path Australian employee chief gives bottom magazines packages detail laws changed pet heard begin individuals Colorado royal clean switch Russian largest African guy titles relevant guidelines justice connect bible cup basket applied weekly installation described demand suite square attention advance skip diet army auction gear lee difference allowed correct nation selling lots piece sheet firm seven older Illinois regulations elements species jump cells module resort facility random pricing certificate minister motion looks fashion directions visitors documentation monitor trading forest calls whose coverage couple giving chance vision ball ending clients actions listen discuss accept automotive goal successful sold wind communities clinical situation sciences markets lowest highly publishing appear emergency developing lives currency leather determine temperature palm announcements patient actual historical stone commerce ringtones perhaps persons difficult scientific satellite fit tests village accounts amateur met pain particularly factors coffee settings buyer cultural easily oral ford poster edge functional root closed holidays ice pink balance monitoring graduate replies shot architecture initial label thinking recommend hardcore league waste minute bus provider optional dictionary cold accounting manufacturing sections chair fishing effort phase fields bag fantasy letters motor professor context install shirt apparel generally continued foot mass crime count techniques quickly dollars websites religion claim driving permission surgery patch heat wild measures generation Kansas miss chemical doctor task reduce brought himself nor component enable exercise bug santa guarantee leader diamond Israel processes soft servers alone meetings seconds Arizona keyword interests flight Congress fuel username walk produced Italian paperback wait supported pocket saint rose freedom argument competition creating drugs joint premium providers fresh characters attorney upgrade factor growing thousands stream apartments pick hearing eastern auctions therapy entries dates generated signed upper administrative serious prime limit began steps errors shops bondage efforts informed thoughts creek worked quantity urban practices sorted reporting essential myself tours platform load affiliate labor immediately admin nursing defense machines designated tags heavy covered recovery guys integrated configuration merchant comprehensive expert universal protect drop solid presentation languages became orange compliance vehicles prevent theme rich campaign marine improvement guitar finding Pennsylvania examples saying spirit claims challenge acceptance strategies seem affairs touch intended towards goals hire election suggest branch charges serve affiliates reasons magic mount smart talking gave ones Latin multimedia avoid certified manage corner rank computing Oregon element birth virus abuse interactive requests separate quarter procedure leadership tables define racing religious facts breakfast column plants faith chain developer identify avenue missing died approximately domestic recommendations moved Houston reach comparison mental viewed moment extended sequence inch attack sorry centers opening damage reserve recipes gamma plastic produce snow placed truth counter failure follows weekend dollar camp Ontario automatically Minnesota films bridge native fill movement printing baseball owned approval draft chart played contacts Jesus readers clubs equal adventure matching offering shirts profit leaders posters institutions assistant variable advertisement expect parking headlines yesterday compared determined wholesale workshop Russia gone codes kinds extension Seattle statements golden completely teams fort lighting senate forces funny brother gene turned portable tried electrical applicable disc returned pattern boat named laser earlier manufacturers sponsor classical icon warranty dedicated Indiana direction basketball objects ends delete evening assembly nuclear taxes mouse signal criminal issued brain Wisconsin powerful dream obtained false cast flower felt personnel passed supplied identified falls soul aids opinions promote stated stats Hawaii professionals appears carry flag decided covers advantage hello designs maintain tourism priority newsletters adults clips savings graphic atom payments estimated binding brief ended winning eight anonymous iron straight script served wants miscellaneous prepared void dining alert integration Atlanta tag interview mix framework disk installed queen credits clearly fix handle sweet desk criteria Massachusetts vice associate truck behavior enlarge ray frequently revenue measure changing votes duty looked discussions bear gain festival laboratory ocean flights experts signs lack depth whatever logged laptop vintage train exactly dry explore concept nearly eligible checkout reality forgot handling origin knew gaming feeds billion destination Scotland faster intelligence Dallas bought con nations route followed specifications broken Alaska zoom blow battle residential anime speak decisions industries protocol query clip partnership editorial expression equity provisions speech wire principles suggestions rural shared sounds replacement tape strategic judge spam economics acid bytes cent forced compatible fight apartment height null zero speaker filed Netherlands obtain consulting recreation offices designer remain managed failed marriage roll Korea banks participants secret bath leads negative favorites Toronto theater Missouri perform healthy translation estimates font assets injury ministry drivers lawyer figures married protected proposal sharing Philadelphia portal waiting birthday beta fail banking officials toward won slightly assist conduct contained legislation calling parameters jazz serving bags profiles Miami comics matters houses postal relationships Tennessee wear controls breaking combined ultimate Wales representative frequency introduced minor finish departments residents noted displayed reduced physics rare spent performed extreme samples bars reviewed row forecast removed helps singles administrator cycle amounts contain accuracy dual rise sleep bird pharmacy Brazil creation static scene hunter addresses lady crystal famous writer chairman violence fans Oklahoma speakers drink academy dynamic gender eat permanent agriculture dell cleaning constitutes portfolio practical delivered collectibles infrastructure exclusive seat concerns vendor originally intel utilities philosophy regulation officers reduction aim bids referred supports nutrition recording regions junior toll cape rings meaning secondary wonderful mine ladies ticket announced guess agreed prevention whom ski soccer math import posting presence instant mentioned automatic healthcare viewing maintained increasing majority connected Christ dogs directors aspects Austria ahead moon participation scheme utility preview fly manner matrix containing combination amendment despite strength guaranteed Turkey libraries proper distributed degrees Singapore enterprises delta fear seeking inches phoenix convention shares principal daughter standing comfort colors wars ordering kept alpha appeal cruise bonus certification previously hey bookmark buildings specials beat household batteries smoking becomes drives arms Alabama tea improved trees achieve positions dress subscription dealer contemporary sky nearby carried happen exposure hide signature gambling refer miller provision outdoors clothes caused luxury babes frames certainly indeed newspaper toy circuit layer printed slow removal easier liability trademark hip printers nine adding Kentucky mostly spot trackback prints spend factory interior revised grow Americans optical promotion relative amazing clock dot identity suites conversion feeling hidden reasonable Victoria serial relief revision broadband influence ratio importance rain onto planet webmaster copies recipe permit seeing proof tennis bass prescription bedroom empty instance hole pets ride licensed Orlando specifically bureau Maine represent conservation pair ideal recorded pieces finished parks dinner lawyers Sydney stress cream runs trends discover patterns boxes Louisiana hills fourth advisor marketplace evil aware shape evolution Irish certificates objectives stations suggested remains greatest firms concerned euro operator structures generic encyclopedia usage cap ink charts continuing mixed census interracial peak competitive exist wheel transit suppliers salt compact poetry lights tracking angel bell keeping preparation attempt receiving matches accordance width noise engines forget array discussed accurate climate reservations pin PlayStation alcohol Greek instruction managing annotation sister raw differences walking explain smaller newest establish gnu happened expressed extent sharp lane paragraph kill mathematics compensation export managers aircraft modules Sweden conflict conducted versions employer occur percentage knows Mississippi describe concern backup requested citizens Connecticut heritage immediate holding trouble spread coach agricultural expand supporting audience assigned collections ages participate plug specialist cook affect virgin experienced investigation raised hat institution directed dealers searching sporting helping perl affected bike totally plate expenses indicate blonde proceedings transmission characteristics lose organic seek experiences albums cheats extremely contracts guests hosted diseases concerning developers equivalent chemistry neighborhood Nevada kits Thailand variables agenda anyway continues tracks advisory curriculum logic template prince circle soil grants anywhere psychology responses Atlantic wet circumstances investor identification leaving wildlife appliances matt elementary cooking speaking sponsors fox unlimited respond sizes plain exit entered Iran arm keys launch wave checking Belgium printable holy acts guidance mesh trail enforcement symbol crafts highway buddy hardcover observed dean setup poll booking glossary fiscal celebrity styles Denver filled bond channels appendix notify blues chocolate pub portion scope Hampshire supplier cables cotton bluetooth controlled requirement authorities biology dental killed border ancient debate representatives starts pregnancy causes Arkansas biography leisure attractions learned transactions notebook explorer historic attached opened husband disabled authorized crazy upcoming Britain concert retirement scores financing efficiency comedy adopted efficient weblog linear commitment specialty bears jean hop carrier edited constant visa mouth jewish meter linked Portland interviews concepts gun reflect pure deliver wonder hell lessons fruit begins qualified reform lens alerts treated discovery draw classified relating assume confidence alliance confirm warm neither offline leaves engineer lifestyle consistent replace clearance connections inventory converter babe checks reached becoming safari objective indicated sugar crew legs stick securities relation enabled genre slide Montana volunteer tested rear democratic enhance Switzerland exact bound parameter adapter processor node formal dimensions contribute lock hockey storm micro colleges laptops mile showed challenges editors threads bowl supreme brothers recognition presents tank submission dolls estimate encourage navy kid regulatory inspection consumers cancel limits territory transaction Manchester paint delay pilot outlet contributions continuous Czech resulting Cambridge initiative novel pan execution disability increases ultra winner Idaho contractor episode examination potter dish plays bulletin indicates modify Oxford truly painting committed extensive affordable universe candidate databases patent slot outstanding eating perspective planned watching lodge messenger mirror tournament consideration discounts sessions kernel stocks buyers journals gray catalogue charged broad Taiwan chosen demo Greece Swiss hate terminal publishers nights behalf Caribbean liquid rice Nebraska loop salary reservation foods gourmet guard properly saving remaining empire resume twenty newly raise prepare avatar depending illegal expansion vary hundreds Rome Arab helped premier tomorrow purchased milk decide consent drama visiting performing downtown keyboard contest collected bands boot suitable absolutely millions lunch audit push chamber findings muscle featuring implement clicking scheduled polls typical tower yours sum calculator significantly chicken temporary attend shower sending tonight dear sufficient shell province catholic oak vat awareness Vancouver governor beer seemed contribution measurement swimming spyware formula constitution packaging solar catch Pakistan reliable consultation northwest sir doubt earn finder unable periods classroom tasks democracy attacks wallpaper merchandise resistance doors symptoms resorts biggest memorial visitor twin forth insert Baltimore gateway alumni drawing candidates ordered biological fighting transition happens preferences spy romance instrument split themes powers heaven bits pregnant twice classification focused Egypt physician bargain cellular Norway Vermont asking blocks normally spiritual hunting diabetes suit shift chip sit bodies photographs cutting wow writers marks flexible loved mapping numerous relatively birds satisfaction represents indexed Pittsburgh superior preferred saved paying cartoon shots intellectual granted choices carbon spending comfortable magnetic interaction listening effectively registry crisis outlook massive Denmark employed bright treat header poverty formed piano echo grid sheets experimental revolution consolidation displays plasma allowing earnings mystery landscape dependent mechanical journey Delaware bidding consultants risks banner applicant charter fig cooperation counties acquisition ports implemented directories recognized dreams blogger notification licensing stands teach occurred textbooks rapid pull hairy diversity Cleveland reverse deposit seminar investments Latina wheels specify accessibility Dutch sensitive templates formats tab depends boots holds router concrete editing Poland folder completion upload pulse universities technique contractors voting courts notices subscriptions calculate Detroit broadcast converted metro anniversary improvements strip specification pearl accident nick accessible accessory resident plot possibly airline typically representation regard pump exists arrangements smooth conferences strike consumption Birmingham flashing narrow afternoon surveys sitting putting consultant controller ownership committees legislative researchers Vietnam trailer castle gardens missed Malaysia unsubscribe antique labels willing molecular acting heads stored exam logos residence attorneys antiques density hundred operators strange sustainable Philippines statistical beds mention innovation employers grey parallel amended operate bills bold bathroom stable opera definitions doctors lesson cinema asset scan elections drinking reaction blank enhanced entitled severe generate stainless newspapers hospitals deluxe humor aged monitors exception lived duration bulk successfully Indonesia pursuant fabric visits primarily tight domains capabilities contrast recommendation flying recruitment sin Berlin cute organized adoption improving expensive meant capture pounds buffalo plane explained seed desire expertise mechanism camping meets welfare peer caught eventually marked driven measured bottle agreements considering innovative marshall massage rubber conclusion closing thousand meat legend grace python monster bang villa bone columns disorders bugs collaboration detection cookies inner formation tutorial engineers entity cruises gate holder proposals moderator tutorials settlement Portugal Roman duties valuable erotic tone collectables ethics forever dragon busy captain fantastic imagine brings heating leg neck wing governments purchasing scripts stereo appointed taste dealing commit tiny operational rail airlines liberal trips gap sides tube turns corresponding descriptions cache belt jacket determination animation oracle lease productions aviation hobbies proud excess disaster console commands telecommunications instructor giant achieved injuries shipped seats approaches biz alarm voltage usual loading stamps appeared angle rob vinyl highlights mining designers Melbourne ongoing worst imaging betting scientists liberty blackjack Argentina era convert possibility analyst commissioner dangerous garage exciting reliability thongs unfortunately respectively volunteers attachment ringtone Finland derived pleasure honor asp oriented eagle desktops pants nurse prayer appointment workshops hurricane quiet luck postage producer represented mortgages dial responsibilities cheese comic carefully jet productivity investors crown underground diagnosis maker crack principle picks vacations gang semester calculated fetish applies casinos appearance smoke filters incorporated craft cake notebooks apart fellow blind lounge mad algorithm semi coins gross strongly cafe valentine proteins horror familiar capable involving pen investing admission shoe elected carrying victory sand terrorism joy editions mainly ethnic ran parliament actor finds seal situations fifth allocated citizen vertical corrections structural municipal describes prize occurs absolute disabilities consists anytime substance prohibited addressed lies pipe soldiers guardian lecture simulation layout initiatives ill concentration classics lay interpretation horses dirty deck donate taught bankruptcy worker optimization alive temple substances prove discovered wings breaks genetic restrictions participating waters promise thin exhibition prefer ridge cabinet modem bringing sick dose evaluate tropical collect bet composition streets nationwide vector definitely shaved turning buffer purple existence commentary limousines developments def immigration destinations lets mutual pipeline necessarily syntax attribute prison skill chairs everyday apparently surrounding mountains moves popularity inquiry ethernet checked exhibit throw trend sierra visible cats desert oldest coordinator obviously mercury handbook navigate worse summit victims spaces fundamental burning escape coupons somewhat receiver substantial progressive boats glance Scottish championship arcade impossible tells obvious fiber depression graph covering platinum judgment bedrooms talks filing foster modeling passing awarded testimonials trials tissue memorabilia masters bonds cartridge explanation folk commons Cincinnati subsection fraud electricity permitted spectrum arrival okay pottery emphasis aspect workplace awesome Mexican confirmed counts priced wallpapers crash lift desired inter closer assumes heights shadow riding infection expense grove eligibility venture clinic Korean healing princess mall entering packet spray studios involvement dad buttons placement observations funded winners extend roads subsequent pat Dublin rolling fell motorcycle yard disclosure establishment memories arrived creates faces tourist mayor murder adequate senator yield presentations grades cartoons pour digest lodging dust hence entirely replaced radar rescue undergraduate losses combat reducing stopped occupation lakes donations associations closely radiation diary seriously kings shooting Kent adds ear flags baker launched elsewhere pollution conservative guestbook shock effectiveness walls abroad ebony tie ward drawn visited roof walker demonstrate atmosphere suggests kiss beast operated experiment targets overseas purchases dodge counsel federation pizza invited yards assignment chemicals mod farmers queries rush Ukraine absence nearest cluster vendors whereas yoga serves woods surprise lamp partial shoppers everybody couples Nashville ranking jokes sublime counseling palace acceptable satisfied glad wins measurements verify globe trusted copper rack medication warehouse shareware receipt supposed ordinary nobody ghost violation configure stability applying southwest boss pride institutional expectations independence knowing reporter metabolism champion cloudy personally Chile plenty solo sentence throat ignore uniform excellence wealth tall somewhere vacuum dancing attributes recognize brass writes plaza outcomes survival quest publish screening toe thumbnail whenever nova lifetime pioneer booty forgotten acrobat plates acres venue athletic thermal essays vital telling fairly coastal charity intelligent Edinburgh excel modes obligation wake stupid harbor traveler segment realize regardless enemy puzzle rising wells opens insight restricted Republican secrets lucky latter merchants thick trailers repeat syndrome attendance penalty drum glasses enables Iraqi builder vista chips flood foto ease arguments Amsterdam arena adventures pupils announcement tabs outcome appreciate expanded casual grown Polish lovely extras clause smile lands troops indoor Bulgaria armed broker charger regularly believed pine cooling tend gulf trucks mechanisms divorce shopper Tokyo partly customize tradition candy pills tiger folks sensor exposed hunt angels deputy indicators sealed Thai emissions physicians loaded complaint scenes experiments balls Afghanistan boost scholarship governance mill founded supplements chronic icons moral den catering finger keeps pound locate camcorder trained burn implementing roses ourselves bread tobacco wooden motors tough incident dynamics lie conversation decrease chest pension revenues emerging worship capability herself producing churches precision damages reserves contributed solve shorts reproduction minority diverse amp ingredients sole franchise recorder complaints facing promotions tones passion rehabilitation maintaining sight laid clay patches weak refund towns environments divided reception wise emails Cyprus odds correctly insider seminars consequences makers hearts geography appearing integrity worry discrimination Carter legacy pleased danger vitamin widely processed phrase genuine raising implications functionality paradise hybrid reads roles intermediate emotional sons leaf pad glory platforms bigger billing diesel versus combine overnight geographic exceed rod fault Cuba preliminary districts introduce silk promotional babies compiled romantic revealed specialists generator examine suspension sad correction wolf slowly authentication communicate rugby supplement showtimes portions infant promoting sectors fluid grounds fits kick regards meal hurt machinery bandwidth unlike equation baskets probability pot dimension wright proven schedules admissions cached warren slip studied reviewer involves quarterly profits devil grass comply florist illustrated cherry continental alternate achievement limitations Kenya webcam cuts funeral earrings enjoyed automated chapters Quebec passenger convenient Mars sized noticed socket silent literary egg signals caps orientation pill theft childhood swing symbols meta humans analog facial choosing talent dated flexibility seeker wisdom shoot boundary mint offset payday elite spin holders believes Swedish poems deadline jurisdiction robot displaying witness equipped stages encouraged powder Broadway acquired assess wash cartridges stones entrance gnome roots declaration losing attempts gadgets noble Glasgow automation impacts gospel advantages shore loves induced knight preparing loose aims recipient linking extensions appeals earned illness Islamic athletics southeast ho alternatives pending determining Lebanon personalized conditioning teenage soap triple cooper jam secured unusual answered partnerships destruction slots increasingly migration disorder routine toolbar basically rocks conventional titans applicants wearing axis sought genes mounted habitat firewall median guns scanner herein occupational animated judicial adjustment hero integer treatments bachelor attitude camcorders engaged falling basics Montreal carpet lenses binary genetics attended difficulty punk collective coalition dropped enrollment duke pace besides wage producers collector arc hosts interfaces advertisers moments atlas strings dawn representing observation feels deleted coat restoration convenience returning opposition container defendant confirmation app embedded supervisor wizard corps actors liver peripherals liable brochure morris petition recall antenna picked assumed departure belief killing bikini Memphis shoulder decor lookup texts brokers diameter Ottawa doll podcast seasons Peru interactions refine bidder singer literacy fails aging intervention plugin attraction diving invite modification Latinas suppose customized reed involve moderate terror younger thirty mice opposite understood rapidly ban assurance clerk happening vast mills outline amendments tramadol Holland receives jeans metropolitan compilation verification fonts odd wrap refers mood favor veterans quiz sigma attractive occasion recordings victim demands sleeping careful beam gardening obligations arrive orchestra sunset tracked moreover minimal polyphonic lottery tops framed aside outsourcing adjustable allocation essay discipline demonstrated dialogue identifying alphabetical camps declared dispatched handheld trace disposal shut florists packs installing switches Romania voluntary consult greatly blogging mask cycling midnight commonly photographer inform Turkish coal cry messaging quantum intent zoo largely pleasant announce constructed additions requiring spoke arrow engagement sampling rough weird tee refinance lion inspired holes weddings blade suddenly oxygen cookie meals canyon meters merely calendars arrangement conclusions passes bibliography pointer compatibility stretch Durham furthermore permits cooperative Muslim sleeve cleaner cricket beef feeding stroke township rankings measuring cad hats headquarters crowd transfers surf olympic transformation remained attachments entities customs administrators personality rainbow hook decline gloves Israeli medicare cord skiing cloud facilitate subscriber valve explains proceed feelings knife Jamaica priorities shelf bookstore timing liked parenting adopt denied fotos incredible freeware donation outer crop deaths rivers commonwealth pharmaceutical Manhattan tales workforce Islam nodes thumbs seeds cited lite hub targeted organizational realized twelve founder decade dispute Portuguese tired adverse everywhere excerpt steam discharge drinks voices acute halloween climbing stood sing tons perfume honest Albany hazardous restore stack methodology somebody sue housewares reputation resistant democrats recycling hang curve creator amber qualifications museums coding tracker variation passage transferred trunk hiking damn headset photograph Colombia waves camel distributor lamps underlying hood wrestling archived photoshop Arabia gathering projection juice chase mathematical logical sauce fame extract specialized diagnostic Panama Indianapolis payable corporations courtesy criticism automobile confidential statutory accommodations Athens northeast downloaded judges retired remarks detected decades paintings walked arising bracelet eggs juvenile injection populations protective afraid acoustic railway cassette initially indicator pointed causing mistake locked eliminate fusion mineral sunglasses ruby steering beads fortune preference canvas threshold claimed screens cemetery planner Croatia flows stadium Venezuela exploration fewer sequences"}
            ],
            "hotkey_increase_opacity": "Alt+Up",
            "hotkey_decrease_opacity": "Alt+Down",
            "hotkey_toggle_stats": "`",
            "hotkey_toggle_about": "/",
            "hotkey_cycle_theme_left": "Alt+Left",
            "hotkey_cycle_theme_right": "Alt+Right",
            "hotkey_cycle_mode_left": "Left",
            "hotkey_cycle_mode_right": "Right",
            "hotkey_cycle_option_up": "Up",
            "hotkey_cycle_option_down": "Down",
            "hotkey_cycle_test_up": "Ctrl+Up",
            "hotkey_cycle_test_down": "Ctrl+Down",
            "hotkey_align_left": "Ctrl+Alt+Left",
            "hotkey_align_center": "Ctrl+Alt+Right",
            "themes": [
                {
                    "name": "Default Dark",
                    "primary": "#ffffff",
                    "secondary": "#808080",
                    "error": "#FF0000",
                    "window": "#000000"
                },
                {
                    "name": "Ocean Blue",
                    "primary": "#5b8dd9",
                    "secondary": "#56b6c2",
                    "error": "#e06c75",
                    "window": "#1a2332"
                },
                {
                    "name": "Solarized Dark",
                    "primary": "#657b83",
                    "secondary": "#268bd2",
                    "error": "#dc322f",
                    "window": "#002b36"
                },
                {
                    "name": "High Contrast",
                    "primary": "#ffffff",
                    "secondary": "#ffff00",
                    "error": "#ff4444",
                    "window": "#000000"
                },
                {
                    "name": "Forest Green",
                    "primary": "#98a875",
                    "secondary": "#7ec850",
                    "error": "#e06c75",
                    "window": "#1e2d1e"
                },
                {
                    "name": "Midnight Purple",
                    "primary": "#9d8fff",
                    "secondary": "#c678dd",
                    "error": "#ff5370",
                    "window": "#1a1a2e"
                },
                {
                    "name": "Amber Terminal",
                    "primary": "#b8860b",
                    "secondary": "#ffb300",
                    "error": "#ff4444",
                    "window": "#0d0d00"
                },
                {
                    "name": "Nord",
                    "primary": "#88c0d0",
                    "secondary": "#4c566a",
                    "error": "#bf616a",
                    "window": "#2e3440"
                },
                {
                    "name": "Material Midnight",
                    "primary": "#80cbc4",
                    "secondary": "#82aaff",
                    "error": "#f07178",
                    "window": "#0d1117"
                },
                {
                    "name": "Material Sunset",
                    "primary": "#ffcc80",
                    "secondary": "#ff8a65",
                    "error": "#e57373",
                    "window": "#1f1b24"
                },
                {
                    "name": "Material Ocean",
                    "primary": "#80deea",
                    "secondary": "#40c4ff",
                    "error": "#ff5252",
                    "window": "#0e1a2b"
                },
                {
                    "name": "Material Mint",
                    "primary": "#a5d6a7",
                    "secondary": "#69f0ae",
                    "error": "#ff8a80",
                    "window": "#0f1d1a"
                },
                {
                    "name": "Material Lavender",
                    "primary": "#d1c4e9",
                    "secondary": "#b388ff",
                    "error": "#ff80ab",
                    "window": "#1b1623"
                },
                {
                    "name": "Material Amber",
                    "primary": "#ffe082",
                    "secondary": "#ffd54f",
                    "error": "#ff8a65",
                    "window": "#201a10"
                },
                {
                    "name": "Material Rose",
                    "primary": "#f8bbd0",
                    "secondary": "#f48fb1",
                    "error": "#ef5350",
                    "window": "#241117"
                },
                {
                    "name": "Material Graphite",
                    "primary": "#b0bec5",
                    "secondary": "#90a4ae",
                    "error": "#ff7043",
                    "window": "#1c1c1c"
                },
                {
                    "name": "Material Candy",
                    "primary": "#b2ebf2",
                    "secondary": "#ea80fc",
                    "error": "#ff5252",
                    "window": "#1a1420"
                },
                {
                    "name": "Material Cobalt",
                    "primary": "#90caf9",
                    "secondary": "#448aff",
                    "error": "#ff5252",
                    "window": "#0d1b2a"
                },
                {
                    "name": "Silk",
                    "primary": "#ffffff",
                    "secondary": "#ff8fab",
                    "error": "#ff5252",
                    "window": "#2b1b3d"
                },
                {
                    "name": "People",
                    "primary": "#9be8f5",
                    "secondary": "#f5a9d8",
                    "error": "#ff5252",
                    "window": "#12263a"
                },
                {
                    "name": "Humans",
                    "primary": "#ffd9a3",
                    "secondary": "#f472b6",
                    "error": "#ef4444",
                    "window": "#331c2a"
                },
                {
                    "name": "Friends",
                    "primary": "#fffb82",
                    "secondary": "#9d8cff",
                    "error": "#f97316",
                    "window": "#1a1a24"
                },
                {
                    "name": "Comrades",
                    "primary": "#c4c4c4",
                    "secondary": "#b388ff",
                    "error": "#e57373",
                    "window": "#191921"
                },
                {
                    "name": "Paper White",
                    "primary": "#9e9e9e",
                    "secondary": "#212121",
                    "error": "#d32f2f",
                    "window": "#f5f5f5"
                },
                {
                    "name": "Cloud",
                    "primary": "#90a4ae",
                    "secondary": "#263238",
                    "error": "#e53935",
                    "window": "#eef2f7"
                },
                {
                    "name": "Linen",
                    "primary": "#bcaaa4",
                    "secondary": "#3e2723",
                    "error": "#c62828",
                    "window": "#faf6f0"
                },
                {
                    "name": "Mint Cream",
                    "primary": "#80cbc4",
                    "secondary": "#1b5e20",
                    "error": "#c62828",
                    "window": "#f0f7f4"
                },
                {
                    "name": "Lavender Mist",
                    "primary": "#b39ddb",
                    "secondary": "#311b92",
                    "error": "#c62828",
                    "window": "#f5f2fa"
                },
                {
                    "name": "Sky",
                    "primary": "#81d4fa",
                    "secondary": "#0d47a1",
                    "error": "#c62828",
                    "window": "#eef6fb"
                },
                {
                    "name": "Sand",
                    "primary": "#d7ccc8",
                    "secondary": "#4e342e",
                    "error": "#c62828",
                    "window": "#faf5ec"
                },
                {
                    "name": "Rose Petal",
                    "primary": "#f48fb1",
                    "secondary": "#880e4f",
                    "error": "#c62828",
                    "window": "#fdf2f4"
                },
                {
                    "name": "Slate",
                    "primary": "#b0bec5",
                    "secondary": "#37474f",
                    "error": "#c62828",
                    "window": "#eceff1"
                },
                {
                    "name": "Butter",
                    "primary": "#ffe082",
                    "secondary": "#5d4037",
                    "error": "#c62828",
                    "window": "#fdf9e9"
                },
                {
                    "name": "Neon Sunset",
                    "primary": "#ffea00",
                    "secondary": "#ffffff",
                    "error": "#000000",
                    "window": "#ff3d00"
                },
                {
                    "name": "Electric Violet",
                    "primary": "#00e5ff",
                    "secondary": "#ffffff",
                    "error": "#ff1744",
                    "window": "#7c4dff"
                },
                {
                    "name": "Cyber Lime",
                    "primary": "#00b0ff",
                    "secondary": "#1a237e",
                    "error": "#ff1744",
                    "window": "#00e676"
                },
                {
                    "name": "Hot Magenta",
                    "primary": "#00e5ff",
                    "secondary": "#ffffff",
                    "error": "#000000",
                    "window": "#f50057"
                },
                {
                    "name": "Tangerine",
                    "primary": "#ffea00",
                    "secondary": "#3e2723",
                    "error": "#d50000",
                    "window": "#ff9100"
                },
                {
                    "name": "Aqua Pop",
                    "primary": "#ffea00",
                    "secondary": "#ffffff",
                    "error": "#d50000",
                    "window": "#00b8d4"
                },
                {
                    "name": "Grape Soda",
                    "primary": "#ffea00",
                    "secondary": "#ffffff",
                    "error": "#000000",
                    "window": "#aa00ff"
                },
                {
                    "name": "Crimson",
                    "primary": "#ffea00",
                    "secondary": "#ffffff",
                    "error": "#000000",
                    "window": "#d50000"
                },
                {
                    "name": "Ocean Wave",
                    "primary": "#00e676",
                    "secondary": "#ffffff",
                    "error": "#d50000",
                    "window": "#00b0ff"
                },
                {
                    "name": "Sunshine",
                    "primary": "#ff3d00",
                    "secondary": "#1a237e",
                    "error": "#d50000",
                    "window": "#ffd600"
                },
                {
                    "name": "Espresso",
                    "primary": "#d7ccc8",
                    "secondary": "#efebe9",
                    "error": "#ff8a80",
                    "window": "#3e2723"
                },
                {
                    "name": "Cappuccino",
                    "primary": "#bcaaa4",
                    "secondary": "#f5f5f5",
                    "error": "#ff8a80",
                    "window": "#4e342e"
                },
                {
                    "name": "Mocha",
                    "primary": "#a1887f",
                    "secondary": "#d7ccc8",
                    "error": "#ff8a80",
                    "window": "#2d1f1a"
                },
                {
                    "name": "Java",
                    "primary": "#8d6e63",
                    "secondary": "#d7ccc8",
                    "error": "#ff8a80",
                    "window": "#1f1410"
                },
                {
                    "name": "Caramel",
                    "primary": "#ffcc80",
                    "secondary": "#4e342e",
                    "error": "#c62828",
                    "window": "#5d4037"
                },
                {
                    "name": "Grey Fog",
                    "primary": "#bdbdbd",
                    "secondary": "#fafafa",
                    "error": "#ef5350",
                    "window": "#424242"
                },
                {
                    "name": "Silver",
                    "primary": "#e0e0e0",
                    "secondary": "#ffffff",
                    "error": "#ef5350",
                    "window": "#616161"
                },
                {
                    "name": "Graphite Grey",
                    "primary": "#9e9e9e",
                    "secondary": "#eeeeee",
                    "error": "#ef5350",
                    "window": "#212121"
                },
                {
                    "name": "Stone",
                    "primary": "#b0bec5",
                    "secondary": "#eceff1",
                    "error": "#ef5350",
                    "window": "#37474f"
                },
                {
                    "name": "Ash",
                    "primary": "#cfd8dc",
                    "secondary": "#ffffff",
                    "error": "#ef5350",
                    "window": "#263238"
                },
                {
                    "name": "Midnight",
                    "primary": "#9e9e9e",
                    "secondary": "#e0e0e0",
                    "error": "#ef5350",
                    "window": "#000000"
                },
                {
                    "name": "Void",
                    "primary": "#bdbdbd",
                    "secondary": "#f5f5f5",
                    "error": "#ef5350",
                    "window": "#050505"
                },
                {
                    "name": "Onyx",
                    "primary": "#a0a0a0",
                    "secondary": "#d0d0d0",
                    "error": "#ef5350",
                    "window": "#0a0a0a"
                },
                {
                    "name": "Charcoal",
                    "primary": "#8a8a8a",
                    "secondary": "#c0c0c0",
                    "error": "#ef5350",
                    "window": "#101010"
                },
                {
                    "name": "Pitch",
                    "primary": "#7a7a7a",
                    "secondary": "#b0b0b0",
                    "error": "#ef5350",
                    "window": "#000000"
                }
            ],
            "custom_themes": []
        }
    
    def load(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                loaded: Dict[str, Any] = json.load(f)
                # The built-in theme list always comes from the app version so
                # that new releases can add themes. Only the current theme (the
                # four color keys) and any user-created custom themes persist.
                loaded.pop("themes", None)
                self.settings.update(loaded)
    
    def save(self) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        # The built-in theme list is not persisted; it always comes from the
        # app version. Only the current theme colors and custom themes save.
        to_save = {k: v for k, v in self.settings.items() if k != "themes"}
        with open(self.config_path, 'w') as f:
            json.dump(to_save, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.settings[key] = value

    def get_themes(self) -> list:
        """
        Return all available themes: the built-in defaults (from the app
        version) plus any user-created custom themes.
        """
        built_in = self.settings.get("themes", [])
        custom = self.settings.get("custom_themes", [])
        return list(built_in) + list(custom)

    def set_custom_themes(self, themes: list) -> None:
        """Persist the user-created theme list."""
        self.settings["custom_themes"] = themes
