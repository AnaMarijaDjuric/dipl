from pyteal import *
import program

def approval():
    # ko su nasi ucesnici
    # ko je nas opponent
    # sta mi igramo (rock paper scissors)
    # ko je nas oponent - suparnik - protivnik

    # ovo su glavne varijable koje cemo mi koristiti
    local_sender = Bytes("opponent")                                                        #byteslice
    local_chosenBook = Bytes("book")                                                                #byteslice
    local_fee = Bytes("wager")                                                                      #uint64
    local_hash_info = Bytes("hashed_info")                                                  #byt
    local_real_info = Bytes("real_info")
    # local_result = Bytes("result") #byt
    # ova poslednja varijavla mi mozda ne treba


    op_start=Bytes("start")             #pocinje kupovina
    op_accept=Bytes("accept")               #prihvataju kupovinu (placanje ili mozda slanje spiska knjiga koji zeli da kupi) msm da je ipak ovo drugo
    op_resolve=Bytes("resolve")             #vraca da li je kupovina uspesna ili nema dovoljno sredstava na racunu



    @Subroutine(TealType.none)
    def get_ready(account: Expr):
        return Seq(
            App.localPut(account,local_sender,Bytes("")),
            App.localPut(account,local_chosenBook,Bytes("")),
            App.localPut(account,local_fee,Int(0)),
            App.localPut(account,local_hash_info,Bytes("")),
            App.localPut(account,local_real_info,Bytes(""))
            # ovo poslednje nisam sigurna da treban OBRISI ZAREZ KOD POSLEDNJEG
            #App.localPut(account,local_result,Bytes(""))
            
        )
    
    @Subroutine(TealType.uint64)
    def check_if_empty(account:Expr):
        return Return(
            And(
                App.localGet(account,local_sender)==Bytes(""),
                App.localGet(account,local_chosenBook)==Bytes(""),
                App.localGet(account,local_fee)==Int(0),
                App.localGet(account,local_hash_info)==Bytes(""),
                App.localGet(account,local_real_info)==Bytes("")
            )
        )
    
    perform_checks = Assert(
        And(
            Global.group_size()==Int(1),
            # provera da li je trenutna transakcija prva
            Txn.group_index()==Int(0),
            Gtxn[0].rekey_to()==Global.zero_address(),     
            # Gtxn[1].rekey_to()==Global.zero_address(),
            # proveravamo da li se opt-inovao samo prvi ucesnik zbog check_if_empty
            App.optedIn(Txn.accounts[1],Global.current_application_id()),

        )
    )
    

    @Subroutine(TealType.none)
    def start_app():
        return Seq(
            # perform_checks,
            Assert(
                Global.group_size()==Int(1),
                # provera da li je trenutna transakcija prva
                Txn.group_index()==Int(0),
                Gtxn[0].rekey_to()==Global.zero_address(),     
                # Gtxn[1].rekey_to()==Global.zero_address(),
                # proveravamo da li se opt-inovao samo prvi ucesnik zbog check_if_empty
                App.optedIn(Txn.accounts[1],Global.current_application_id()),
                # And(
                    check_if_empty(Txn.sender()),
                    check_if_empty(Txn.accounts[1]),
                # )
            ),
            # App.localPut(Txn.sender(),local_chosenBook,Txn.application_args[1]),
            # znaci poenta je da ja kad se opt-inujem prvo saljem pare i svoje informacije pa tek onda kad me prihvate ja saljem izabrane knjige
            # da li je to ispravna logika pa i ne bas

            ## zasto nije ovo pisalo u easyhealth app
            # App.localPut(Txn.sender(), local_sender, Txn.accounts[1]),
            App.localPut(Txn.accounts[1],local_hash_info,Txn.application_args[1]),
            App.localPut(Txn.accounts[1],local_chosenBook,Txn.application_args[2]),
            # App.localPut(Txn.sender(),local_hash_info,Txn.application_args[1]),
            # App.localPut(Txn.sender(),local_chosenBook,Txn.application_args[2]),
            # samo transakcije za placanje imaju Group
            # App.localPut(Txn.sender(),local_fee,Gtxn[1].amount()),
            
            Approve()
        )
    

    
    @Subroutine(TealType.none)
    def accept_app():
        chosen = ScratchVar(TealType.bytes)

        return Seq(
           
            Assert(  #ako treba dodaj and
                And( #dodale
                # Global.group_size()==Int(1),
                # Txn.group_index()==Int(0),
                # Gtxn[0].rekey_to()==Global.zero_address(),
                # # Gtxn[1].rekey_to()==Global.zero_address(),
                # App.optedIn(Txn.accounts[1],Global.current_application_id()),
                Global.group_size()==Int(1),
                # provera da li je trenutna transakcija prva
                Txn.group_index()==Int(0),
                Gtxn[0].rekey_to()==Global.zero_address(),     
                # Gtxn[1].rekey_to()==Global.zero_address(),
                # proveravamo da li se opt-inovao samo prvi ucesnik zbog check_if_empty
                App.optedIn(Txn.accounts[1],Global.current_application_id()),
                # check_testing_fee(local_testing_fee),
            #    check_fee(App.localGet(Txn.accounts[1], local_fee)),
                #check_if_empty(Txn.sender())

                # provera da li je uneo dobro svoje licne podatke
                # App.localGet(Txn.accounts[1], local_hash_info) == Sha256(Txn.application_args[1])
            
            )
            ),
           # ja ovde bukvalno samo kazem e okej stavi u lokalnu varaijablu BIBLIOTEKE da sam se ja (korisnik B) prijavio
           # zapravo ovde kaze stavi u varijablu opponenta tj protivnika tj stavi studenta
            App.localPut(Txn.sender(),local_sender,Txn.accounts[1]),
            # trebalo bi da pokusam i da uzmem ono sto je prvi korisnik (student) stavio kao chosen book
            chosen.store(App.localGet(Txn.accounts[1], local_chosenBook)),

            # App.localPut(Txn.sender(),local_crp,Txn.application_args[1]),
            # App.localPut(Txn.sender(),local_wbc,Txn.application_args[2]),
            # App.localPut(Txn.sender(),local_lym,Txn.application_args[3]),
            # App.localPut(Txn.sender(),local_testing_fee,Gtxn[1].amount()),
            #App.localPut(Txn.sender(),local_hash_LBO,Txn.application_args[4]), #mora hash
            Approve()
   
        )


   
    
    @Subroutine(TealType.none)
    def transfer_money(acc_index:Expr, fee:Expr):
        return Seq(
            # pravimo inner transaction
            # first step
            InnerTxnBuilder.Begin(),

            
            # second step
            InnerTxnBuilder.SetFields({
                TxnField.type_enum:TxnType.Payment,
                TxnField.receiver:Txn.accounts[acc_index],
                TxnField.amount:fee
            }),
            # third step
            InnerTxnBuilder.Submit()
            
        )
    
  
    



    @Subroutine(TealType.none)
    def resolve_app():
       
        shop_fee = ScratchVar(TealType.uint64)
        return Seq(
            
            Assert(
                And(
                    # ja imam dve transakcije jer se ovde placa
                    Global.group_size()==Int(2),
                    Txn.group_index()==Int(0),
                    # nije mi jasno za recievera ali mislim da on mora da postoji kad imamo payment
                    
                    # imam placanje u ovoj funkciji, i imam recievera tj. ostavljam sredstva na account aplikacije
                    # kao kad uplatim sredstva na racun e studenta
                    Gtxn[1].type_enum()==TxnType.Payment,
                    Gtxn[1].receiver()==Global.current_application_address(),

                    # imacemo 2 jer imamo 2 transakcije JER IMAMO PLACANJE SADA
                    Gtxn[0].rekey_to()==Global.zero_address(),
                    Gtxn[1].rekey_to()==Global.zero_address(),


                    #Txn.application_args.length()==Int(3)

                    #provera da li je student dobro uneo svoje licne podatke
                    App.localGet(Txn.accounts[1], local_hash_info) == Sha256(Txn.application_args[1]),

                    
                )
            ),
            App.localPut(Txn.sender(),local_fee,Gtxn[1].amount()),
            # ovo samo da razjasnim jos malo
            shop_fee.store(App.localGet(Txn.accounts[0], local_fee)),

            transfer_money(Int(1), shop_fee.load()),

            # crp.store(Btoi(App.localGet(Txn.accounts[1],local_crp))),
            # wbc.store(Btoi(App.localGet(Txn.accounts[1],local_wbc))),
            # lym.store(Btoi(App.localGet(Txn.accounts[1],local_lym))),
           # lbo.store(App.localGet(Txn.accounts[0],local_real_LBO)),
            # testing_fee.store(App.localGet(Txn.accounts[0],local_testing_fee)),

            # calc_blood(crp.load(),wbc.load(),lym.load()),
            # transfer_wager(Int(1),testing_fee.load()),
            Approve()

        )  

    

    return program.event(
        init=Approve(),
        opt_in=Seq(
          get_ready(Txn.sender()),
          Approve()
        ),
        no_op=Seq(
            Cond(
                [Txn.application_args[0]==op_start,start_app()],
                [Txn.application_args[0]==op_accept,accept_app()],
                [Txn.application_args[0]==op_resolve,resolve_app()]
            )  ,
           Reject()
        )
    )

def clear():
    return Approve()