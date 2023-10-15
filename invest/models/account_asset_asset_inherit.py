import time

import barcode
from odoo import models, fields, api, _
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import logging
import calendar
from datetime import datetime
from barcode import EAN13
from barcode.writer import ImageWriter
# import barcode
from barcode import generate
import base64
import io

from odoo.addons.account_asset.models.account_asset import AccountAssetAsset
from barcode.writer import ImageWriter

from odoo.exceptions import UserError


class AccountAssetAssetInherited(models.Model):
    _inherit = "account.asset.asset"

    cheak_wizard = fields.Boolean(default=False)
    product_id = fields.Many2one(comodel_name='product.template')
    etat_asset_id = fields.Many2one(comodel_name='invest.etat.asset')
    date_sorti = fields.Date()
    affectation_id = fields.Many2one(comodel_name='invest.affectation')
    maintenance_ligne_ids = fields.One2many(comodel_name='invest.maintenance.ligne', inverse_name='asset_id')
    code = fields.Char(string='Compte Comptable', compute='_get_code_from_account')
    ancien_code = fields.Char()
    tva = fields.Float()
    ttc = fields.Float()
    numero_inventaire = fields.Char()
    numero_serie = fields.Char()
    personnel_id = fields.Many2one(comodel_name='hr.employee')
    structure_id = fields.Many2one(comodel_name='hr.department')
    endroit_id_1 = fields.Many2one(comodel_name='invest.endroit')
    affectation_ligne_ids = fields.One2many(comodel_name='invest.affectation', inverse_name='asset_id')

    maintenance_ligne_ids = fields.One2many(comodel_name='invest.maintenance.ligne', inverse_name='asset_id')
    depreciation_ligne2_ids = fields.One2many(comodel_name='invest.depreciation.annuel',
                                              inverse_name='asset_id')
    depreciation_ligne3_ids = fields.One2many(comodel_name='account.asset.depreciation.line',inverse_name='asset_id')
    date_aquisition = fields.Date(required=True)
    # barcode = fields.Char('Barcode')
    barcode_image = fields.Binary(string='Barcode Image')
    company_id = fields.Many2one('res.company')
    faible_valeur = fields.Boolean(default=False)
    annee = fields.Integer()
    name = fields.Char(required=False)
    value = fields.Float(required=False)
    category_id = fields.Many2one('account.asset.category', required=False)
    dictonnaire_id = fields.Many2one(comodel_name='invest.dictonnaire')
    cheak_category = fields.Boolean(default=False)
    type_entrer = fields.Selection([('acquisition', 'Acquisition'), ('transfert_externe', 'Transfert Externe'), ('transfert_depuis_stock', 'Transfert Depuis Stock')]
                                   , required=True, default='acquisition')
    invoice_id = fields.Many2one('account.invoice', string='Invoice', states={'draft': [('readonly', False)]}, copy=False)
    demande_achat = fields.Char()
    date_demande_achat = fields.Date()
    num_bon_commande = fields.Char()
    structure_id_achat = fields.Many2one(comodel_name='hr.department')
    demandeur_achat = fields.Many2one(comodel_name='hr.employee')
    piece_entrer = fields.Char()
    date_piece_entrer = fields.Date()
    date_transfert = fields.Date()
    provenance_bien = fields.Many2one(comodel_name='invest.provenance.bien.asset')
    vnc = fields.Monetary()
    state = fields.Selection(selection_add=[('reforme', 'Reforme')])
    date_reintegration = fields.Date()
    date_propser = fields.Date()
    motif_propostion2 = fields.Char()
    mise_attente2 = fields.Char()
    motif_reintegration = fields.Char()
    # typetest = fields.Many2one(comodel_name='invistissement.type.lieu')



    @api.multi
    def imprimer_etat(self):
        return self.env.ref('invest.action_report_barcode').report_action(self)

    # @api.onchange('product_id')
    # def transfert_product_to_asset(self):
    #     for asset in self:
    #         asset.update({
    #         'category_id': asset.product_id.categ_id.categ_asset.id,
    #         'value': asset.product_id.standard_price,
    #         'name': asset.product_id.name,
    #         })

    # @api.onchange('category_id')
    # def onchange_category(self):
    #     for rec in self:
    #         return {'domain': {'dictonnaire_id': [('category_id1' ,'=', rec.dictonnaire_id.category_id1)]}}
    #
    #

    @api.onchange('category_id')
    def _get_team_id_selection_dictonnaire(self):
        for rec in self:
            domain = []
            team_ids = []
            print(rec.category_id.id)
            # print(self.dictonnaire_id.id)
            team_ids = self.env['invest.dictonnaire'].search([('category_id1.id', '=', rec.category_id.id)])
        if team_ids:
            domain.append(('id', 'in', team_ids.ids))
        else:
            domain = ''
        print(domain)
        return {'domain': {'dictonnaire_id': domain}}

    # def transfert_product_to_asset(self):
    #         for rec in self:
    #             print('')
    #                  rec.name = rec.product_id.name
    #                  rec.value = rec.product_id.standard_price
    #                  rec.category_id = rec.product_id.categ_id.categ_asset.id


    def toggle_this(self):
        for rec in self:
            rec.cheak_wizard = not rec.cheak_wizard

    # @api.constrains('date')
    # def verifier_date_ammortissement(self):
    #     for rech in self:
    #         if rech.date < rech.date_aquisition:
    #             print('test idir')
    #             print(rech.date)
    #             print(rech.date_aquisition)
    #             raise UserError("Date d'ammortissement doit être supérieur à la date d'aquisition")

    @api.constrains('date_sorti')
    def verifier_date_sortie(self):
        for rech in self:
            if rech.date_sorti:
                if rech.date_sorti < rech.date_aquisition:
                    raise UserError("Date de sortie doit être supérieur à la date d'aquisition")
    # @api.multi
    # def import_from_stock(self):
    #     for rec in self:
    #         rec.cheak_wizard = False
    #         import logging
    #         logging.error(rec.cheak_wizard)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'target': 'new',
    #         'name': 'Import Stock',
    #         'view_mode': 'form',
    #         'res_model': 'import.stock',
    #     }

    @api.depends('category_id')
    def _get_code_from_account(self):
        '''function to get automatically the account's code '''
        for rec in self:
            account = rec.env['account.account'].search([('id', '=', rec.category_id.account_asset_id.id)]).code
            rec.code = account
        return account

    @api.multi
    def validate(self, vals):
        vals['annee'] = int(time.strftime('%Y'))
        print(self.read()[0])
        wizard_vals = {
            'date_affectation': self.date_aquisition,
            'cheak_stat': self.state,
        }
        wizard_obj = self.env['affectation.asset']
        wizard = wizard_obj.create(wizard_vals)
        return {
            'name': 'Affectation',
            'type': 'ir.actions.act_window',
            'res_model': 'affectation.asset',
            'view_mode': 'form',
            'target': 'new',
            'res_id': wizard.id,  # Pass the ID of the created wizard record
        }
        # return self.env.ref('invistissement.sortie_asset_affectation').read()[0]
        asset = super(AccountAssetAsset, self).validate()

    # @api.multi
    # def testidir3(self):
    #     print('rabah')
    #     records = self.env['account.asset.asset'].search([])
    #     print('idiroooooo')
    #     print(records)
    #     for rec in records:
    #         if rec.numero_inventaire != '':
    #             print(rec.numero_inventaire)
    #             générer_code_barre(rec)


    @api.model
    def create(self, vals):
        # asset = super(AccountAssetAsset, self.with_context(mail_create_nolog=True)).create(vals)
        """On calcule le numero d'inventaire selon la formule suivante :
        id de la compagne - code de compte comptable de bien immobilier
          - le numéro séquentiel incrémentatif selon le code comptable attribuer - l annee en cours,"""

        asset = super(AccountAssetAssetInherited, self).create(vals)
        # asset.name = asset.dictonnaire_id.designation + ' ' + asset.name
        # if asset.product_id:
        #     asset.name = asset.product_id.name
        #     asset.value = asset.product_id.standard_price
        #     asset.category_id = asset.product_id.categ_id.categ_asset.id

        """ la methode compute_depreciation_board_call va 
        nous permettre de calculer la 'ammortissement de bien immobilier
                """
        compute_depreciation_board_call(self, asset)
        # duplicationObjet(asset)

        return asset

    @api.onchange('dictonnaire_id')
    def get_name_by_dictionnay(self):
        self.name = ''
        if self.dictonnaire_id:
            self.name = self.dictonnaire_id.designation + ' ' + self.name

    @api.onchange('type_entrer')
    def clear_fields_Selection(self):
        self.demande_achat = ''
        self.date_demande_achat = ''
        self.num_bon_commande = ''
        self.structure_id_achat = None
        self.demandeur_achat = None
        self.piece_entrer = ''
        self.date_piece_entrer = ''
        self.date_transfert = ''
        self.provenance_bien = ''
        self.vnc = ''




    @api.multi
    def write(self, vals):
        res = super(AccountAssetAsset, self).write(vals)
        res1 = self.env['account.asset.asset'].search([('id', '=', self.id)])



        # rec.name = res1.name
        # rec.value = rec.product_id.standard_price
        # rec.category_id = rec.product_id.categ_id.categ_asset.id
        """On appelle la methode ci-dessous pour le recalcule
         de l'ammortissement de bien immobilier"""
        if self.etat_asset_id and self.state != "close":
            res1.state = "close"

        if self.state not in ['open', 'close']:
            if res1.category_id:
                compute_depreciation_board_call(self, res1)


    @api.multi
    def affectation(self):
        print("rabah")

    """On affiche la wizard de l'affectation de bien immobilier"""
    def affectaion_asset(self):
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Affectation Asset',
            'view_mode': 'form',
            'res_model': 'affectation.asset',
        }

    def maintenance_asset(self):
        """On affiche la wizard de l insertion des actions de
        maintenance que le bien immobilier a subi """
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Maintenance Asset',
            'view_mode': 'form',
            'res_model': 'maintenance.asset',
        }

    def duplication_asset(self):
        """On affiche la wizard de la duplication de bien immobilier """
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': 'Duplication Asset',
            'view_mode': 'form',
            'res_model': 'duplication.asset',
        }
    # vals['date'] = self._context.get('date_p') or time.strftime('%Y-%m-%d')
    #     def afficherbarCode()


def duplicationObjet(asset):
    """on fait appelle à cette methode pour dupliquer un bien immobilier """

    depreciation_ligne = asset.env['account.asset.asset'].create({
        'name': asset.name,
        'code': asset.code,
        'value': asset.value,
        'category_id': asset.category_id.id,
        'date': asset.date,
        'state': asset.state,                                    
        'active': asset.active,
        'method': asset.method,
        'method_number': asset.method_number,
        'method_period': asset.method_period,
        'method_end': asset.method_end,
        'method_progress_factor': asset.method_progress_factor,
        'prorata': asset.prorata,
        'invoice_id': asset.invoice_id,
        'message_last_post': asset.message_last_post,
        'numero_inventaire': asset.numero_inventaire,
        'barcode_image': asset.barcode_image,
        'tva': asset.tva,
        'ttc': asset.ttc,

    })

@api.model
def compute_depreciation_board_call(self, asset):
    depreciation_line1 = self.env['account.asset.depreciation.line'].search([('id', '=', asset.id)])
    for record in asset.depreciation_line_ids:
        record.unlink()
    for record1 in asset.depreciation_ligne2_ids:
        record1.unlink()
    config = self.env['res.config.settings'].sudo().create({})
    value = config.my_config_value

    """On vérifier si le bien immobilier est considéré comme
     faible valeur ou sinon on passe au calcule de l amortissement"""

    if asset.value >= float(value) and asset.faible_valeur == False:
        if asset.category_id.method_number == 0:
            raise UserError("Vous devez définir le nombre d'année d'amortissement")

        """on fait une vérification sur la méthode utilisé pour le calcule de l'amortissmemnt """
        if asset.method != 'linear':

            """on fait appelle aux deux methodes de calcule d'ammortissement
             mensuellement et annuellemment pour le type degressif """
            degressifMenseul(asset, self)
            degressif(asset, self)
            # degressifAnnuel(asset, self)
        else:
            """on fait appelle aux deux methodes de calcule d'ammortissement
                        mensuellement et annuellemment pour le type Lineair """
            linear(asset, self)
            linearMenseul(asset, self)


def générer_code_barre(asset):
    """Cette methode nous permis de creer un code à barre pour le bien
    immobilier qui stocké sur un champs de type byte"""
    ean = barcode.get('code128', asset.numero_inventaire, writer=ImageWriter())
    buffer = io.BytesIO()
    ean.write(buffer)
    barcode_image = base64.b64encode(buffer.getvalue())

    asset.barcode_image = barcode_image
    return asset.barcode_image

def degressifAnnuel(asset, self):
    domain = []
    depreciation = 0

    for record in asset.depreciation_line_ids:

        mois = datetime.strptime(record.depreciation_date, '%Y-%m-%d').month
        team_ids = []
        # depreciation = record.amount + depreciation
        if mois == 12:
            # record.amount = depreciation
            team_ids = self.env['account.asset.depreciation.line'].search([('id', '=', record.id)])
            domain.append(('id', 'in', team_ids.ids))
            # depreciation = 0
            print(domain)

        # asset.depreciation_ligne3_ids =  [(6, 0, data) for data in domain]
        # asset.depreciation_ligne3_ids = asset.depreciation_ligne3_ids.new(team_ids)
        # asset.depreciation_ligne3_ids = team_ids
    #      asset.depreciation_ligne3_ids = [(6, 0, domain)]
    return {'domain': {'depreciation_ligne3_ids': domain}}


def degressifMenseul(asset, self):
    """Cette methode nous permis de calculer l'amortissement mensuellement pour les biens
    ayant un type d'ammortissement degressif"""
    print(asset.type_entrer)
    if asset.type_entrer == 'transfert_externe':
        montant = asset.vnc
    else:
        montant = asset.value

    raimaining = 0
    team_ids = []
    i = 0
    t = 0
    dateDebut = asset.date
    dateDebut_object = fields.Date.from_string(dateDebut)

    jour = datetime.strptime(dateDebut, '%Y-%m-%d').day
    mois = datetime.strptime(dateDebut, '%Y-%m-%d').month

    if jour > 15:
        mois = mois + 1
    nbrMois = 12 - mois
    nbrMois1 = 12 - mois

    montant2 = 0

    debut_annee = date(dateDebut_object.year, mois, 1)
    debut_fin_mois = debut_annee
    debut_fin = relativedelta(months=0) + debut_annee

    team_ids = self.env['invest.ammortissement.matricielle'].search(
        [('categorie_id', '=', asset.category_id.id)])

    amount = 0
    amount = montant
    montant2 = montant
    j = 0
    l = 0
    res = calendar.monthrange(debut_fin.year, debut_fin.month)
    day = res[1]
    debut_fin_mois = debut_fin_mois + relativedelta(day=day)

    for record in team_ids:
        l = l + 1
        t = 0
        while t < 12:
            if j < (12 * len(team_ids)) - 1:
                t = t + 1
                j = j + 1
                # res = calendar.monthrange(debut_fin.year, debut_fin.month)
                # day = res[1]
                # print('ici')
                # print(day)
                # print('ici')
                # debut_fin_mois = debut_fin_mois + relativedelta(day=day)
                # print('ici1')
                # print(debut_fin_mois)
                # print('ici1')
                depreciation_ligne = self.env['account.asset.depreciation.line'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin_mois,
                    'name': (asset.code or '') + '/' + str(l) + '/' + str(t),
                    'sequence': t,
                    'amount': (montant * record.taux * (1 / 12)),
                    'remaining_value': (montant2 - (montant * record.taux * (1 / 12))),
                    'depreciated_value': ((montant * record.taux * (1 / 12)) + raimaining),
                })

                montant2 = montant2 - depreciation_ligne.amount

                raimaining = depreciation_ligne.depreciated_value

                debut_fin_mois = relativedelta(months=1) + debut_fin_mois
                res = calendar.monthrange(debut_fin_mois.year, debut_fin_mois.month)
                day = res[1]
                debut_fin_mois = debut_fin_mois + relativedelta(day=day)

            else:
                l = l + 1
                t = t + 1
                amount = montant * record.taux * ((1) / 12)
                remaining_value = montant - (montant * record.taux * ((1) / 12))

                dateDebut = debut_fin_mois
                montantDernier = depreciation_ligne.remaining_value
                raimaining = depreciation_ligne.depreciated_value
                res = calendar.monthrange(dateDebut.year, dateDebut.month)
                day = res[1]
                depreciation_ligne = self.env['account.asset.depreciation.line'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin_mois,
                    'name': (asset.code or '') + '/' + str(l) + '/' + str(t),
                    'sequence': t,
                    'amount': montantDernier,
                    'remaining_value': (montant - (montant)),
                    'depreciated_value': ((montantDernier) + raimaining),
                })

        # montant = depreciation_ligne.remaining_value


def degressif(asset, self):
    """Cette methode nous permis de calculer l'amortissement annul pour les biens
       ayant un type d'ammortissement degressif"""
    if asset.type_entrer == 'transfert_externe':
        montant = asset.vnc
    else:
        montant = asset.value
    print(asset.value)
    raimaining = 0
    team_ids = []
    i = 0
    dateDebut = asset.date
    dateDebut_object = fields.Date.from_string(dateDebut)
    jour = datetime.strptime(dateDebut, '%Y-%m-%d').day
    mois = datetime.strptime(dateDebut, '%Y-%m-%d').month
    if jour > 15:
        mois = mois + 1
    nbrMois = 12 - mois
    nbrMois1 = 12 - mois

    debut_annee = date(dateDebut_object.year, mois, 1)
    debut_fin = relativedelta(months=nbrMois) + debut_annee
    remaining_value = montant
    team_ids = self.env['invest.ammortissement.matricielle'].search(
        [('categorie_id', '=', asset.category_id.id)])

    amount = 0
    f=0
    for record in team_ids:
        f = f + 1
        if i < (len(team_ids) - 1):
            i += 1

            res = calendar.monthrange(debut_fin.year, debut_fin.month)
            day = res[1]
            debut_fin2 = debut_fin + relativedelta(day=day)
            nbrMois = nbrMois + 1

            depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                'asset_id': asset.id,
                'depreciation_date': debut_fin2,
                'name': (asset.code or '') + '/' + str(f),
                'sequence': f,
                'amount': ((montant * record.taux * (nbrMois / 12)) + amount),
                'remaining_value': (remaining_value - (montant * record.taux * (nbrMois / 12))),
                'depreciated_value': ((montant * record.taux * (nbrMois / 12)) + raimaining),
            })

            montant2 = depreciation_ligne.remaining_value
            raimaining = depreciation_ligne.depreciated_value
            dateDebut = debut_fin2 + relativedelta(day=1)
            nbrMois = 12 - (nbrMois)
            debut_fin = relativedelta(months=nbrMois) + dateDebut
            res = calendar.monthrange(debut_fin.year, debut_fin.month)
            day = res[1]
            debut_fin2 = debut_fin + relativedelta(day=day)

            amount = montant * record.taux * ((nbrMois) / 12)
            remaining_value = montant2 - (montant * record.taux * ((nbrMois) / 12))
            depreciated_value = (montant * record.taux * ((nbrMois) / 12)) + raimaining

            dateDebut = debut_fin2 + relativedelta(day=1)
            nbrMois = 12 - (nbrMois + 1)
            debut_fin = relativedelta(months=nbrMois + 1) + dateDebut
            # montant = remaining_value
            raimaining = depreciated_value
        else:

            if (12 - nbrMois1 != 1):

                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)
                nbrMois = nbrMois + 1

                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(f),
                    'sequence': f,
                    'amount': ((montant * record.taux * (nbrMois / 12)) + amount),
                    'remaining_value': (remaining_value - (montant * record.taux * (nbrMois / 12))),
                    'depreciated_value': ((montant * record.taux * (nbrMois / 12)) + raimaining),
                })

                # if (12 - nbrMois1 != 0):

                amount = montant * record.taux * ((nbrMois) / 12)
                remaining_value = montant2 - (montant * record.taux * ((nbrMois) / 12))

                dateDebut = debut_fin2 + relativedelta(day=1)
                nbrMois = 12 - nbrMois
                debut_fin = relativedelta(months=nbrMois) + dateDebut
                montantDer = depreciation_ligne.remaining_value
                raimaining = depreciation_ligne.depreciated_value
                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)
                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(f +1),
                    'sequence': f + 1,
                    'amount': (montantDer),
                    'remaining_value': (montant - (montant)),
                    'depreciated_value': ((montantDer) + raimaining),
                })
            else:
                amount = montant * record.taux * ((nbrMois) / 12)
                remaining_value = montant2 - (montant * record.taux * ((nbrMois) / 12))

                dateDebut = debut_fin2 + relativedelta(day=1)
                nbrMois = 12 - nbrMois
                debut_fin = relativedelta(months=nbrMois) + dateDebut
                montantDer= depreciation_ligne.remaining_value
                raimaining = depreciation_ligne.depreciated_value
                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)
                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(f+1),
                    'sequence': f + 1,
                    'amount': (montantDer),
                    'remaining_value': (montant - (montant)),
                    'depreciated_value': ((montantDer) + raimaining),
                })


def linear(asset, self):
    """Cette methode nous permis de calculer l'amortissement annuel pour les biens
       ayant un type d'ammortissement Linear"""
    if asset.type_entrer == 'transfert_externe':
        montant = asset.vnc
    else:
        montant = asset.value
    print(asset.value)
    raimaining = 0
    team_ids = []
    i = 0
    dateDebut = asset.date
    dateDebut_object = fields.Date.from_string(dateDebut)

    # jour = datetime.strptime(dateDebut,'%Y-%m-%d').day
    jour = datetime.strptime(dateDebut, '%Y-%m-%d').day
    mois = datetime.strptime(dateDebut, '%Y-%m-%d').month
    if jour > 15:
        mois = mois + 1
    nbrMois1 = 12 - mois

    debut_annee = date(dateDebut_object.year, mois, 1)
    debut_fin = relativedelta(months=nbrMois1) + debut_annee

    t = 0
    while t <= asset.method_number:

        if i < (asset.method_number):
            i += 1

            if i == 1:

                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)
                nbrMois1 = nbrMois1 + 1

                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(i),
                    'sequence': i,
                    'amount': ((montant / asset.method_number) * (nbrMois1 / 12)),
                    'remaining_value': (montant - ((montant / asset.method_number) * (nbrMois1 / 12))),
                    'depreciated_value': (((montant / asset.method_number) * (nbrMois1 / 12)) + raimaining),
                })

            else:
                dateDebut = debut_fin2 + relativedelta(day=1)
                nbrMois = 12
                debut_fin = relativedelta(months=nbrMois) + dateDebut
                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)

                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(i),
                    'sequence': i,
                    'amount': ((montant / asset.method_number)),
                    'remaining_value': (montant2 - (montant / asset.method_number)),
                    'depreciated_value': ((montant / asset.method_number) + raimaining),
                })
            montant2 = depreciation_ligne.remaining_value
            raimaining = depreciation_ligne.depreciated_value
        else:
            if (12 - nbrMois1 != 0):
                dateDebut = debut_fin2 + relativedelta(day=1)
                nbrMois = 12 - nbrMois1
                debut_fin = relativedelta(months=nbrMois) + dateDebut
                montant = depreciation_ligne.remaining_value
                raimaining = depreciation_ligne.depreciated_value
                res = calendar.monthrange(debut_fin.year, debut_fin.month)
                day = res[1]
                debut_fin2 = debut_fin + relativedelta(day=day)
                depreciation_ligne = self.env['invest.depreciation.annuel'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin2,
                    'name': (asset.code or '') + '/' + str(t + 1),
                    'sequence': t + 1,
                    'amount': montant,
                    'remaining_value': (montant - (montant)),
                    'depreciated_value': ((montant) + raimaining),
                })

        t = t + 1


def linearMenseul(asset, self):
    """Cette methode nous permis de calculer l'amortissement mensuellement pour les biens
       ayant un type d'ammortissement Linear"""
    if asset.type_entrer == 'transfert_externe':
        montant = asset.vnc
    else:
        montant = asset.value
    print(asset.value)
    raimaining = 0
    team_ids = []
    i = 0
    t = 0
    dateDebut = asset.date
    dateDebut_object = fields.Date.from_string(dateDebut)

    jour = datetime.strptime(dateDebut, '%Y-%m-%d').day
    mois = datetime.strptime(dateDebut, '%Y-%m-%d').month
    print(jour)
    print(mois)
    if jour > 15:
        mois = mois + 1
    nbrMois = 12 - mois
    nbrMois1 = 12 - mois
    montant2 = 0
    debut_annee = date(dateDebut_object.year, mois, 1)
    debut_fin_mois = debut_annee
    debut_fin = relativedelta(months=0) + debut_annee
    amount = 0
    amount = montant
    montant2 = montant
    j = 0
    k = 0
    res = calendar.monthrange(debut_fin.year, debut_fin.month)
    day = res[1]
    debut_fin_mois = debut_fin_mois + relativedelta(day=day)
    print('rere1')
    while k < asset.method_number:
        k = k + 1
        t = 0
        while t < 12:
            if j < (12 * asset.method_number) - 1:
                t = t + 1
                j = j + 1
                # res = calendar.monthrange(debut_fin.year, debut_fin.month)
                # day = res[1]
                # debut_fin_mois = debut_fin_mois + relativedelta(day=day)
                # print('rere1')
                depreciation_ligne = self.env['account.asset.depreciation.line'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin_mois,
                    'name': (asset.code or '') + '/' + str(k) + '/' + str(t),
                    'sequence': t,
                    'amount': ((montant * (1 / (12 * asset.method_number)))),
                    'remaining_value': (montant2 - (montant * (1 / (12 * asset.method_number)))),
                    'depreciated_value': ((montant * (1 / (12 * asset.method_number))) + raimaining),
                })

                montant2 = montant2 - depreciation_ligne.amount
                raimaining = depreciation_ligne.depreciated_value
                debut_fin_mois = relativedelta(months=1) + debut_fin_mois
                res = calendar.monthrange(debut_fin_mois.year, debut_fin_mois.month)
                day = res[1]
                debut_fin_mois = debut_fin_mois + relativedelta(day=day)

            else:
                t = t + 1
                amount = montant * ((1) / (12 * asset.method_number))
                remaining_value = montant - (montant * ((1) / (12 * asset.method_number)))
                dateDebut = debut_fin_mois
                montant = depreciation_ligne.remaining_value
                raimaining = depreciation_ligne.depreciated_value
                res = calendar.monthrange(dateDebut.year, dateDebut.month)
                day = res[1]
                depreciation_ligne = self.env['account.asset.depreciation.line'].create({
                    'asset_id': asset.id,
                    'depreciation_date': debut_fin_mois,
                    'name': (asset.code or '') + '/' + str(k) + '/' + str(t),
                    'sequence': t,
                    'amount': montant,
                    'remaining_value': (montant - (montant)),
                    'depreciated_value': ((montant) + raimaining),
                })



# def validateAffect(self):
#     return {
#         'type': 'ir.actions.act_window',
#         'target': 'new',
#         'name': 'Affectation Asset',
#         'view_mode': 'form',
#         'res_model': 'affectation.asset',
#     }
