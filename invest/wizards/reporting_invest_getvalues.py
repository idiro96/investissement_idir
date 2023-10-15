# -*- coding: utf-8 -*-
from datetime import datetime
from itertools import groupby

from odoo import models, fields, api


class invistissementGetValuesRepertoireAsset(models.AbstractModel):
    _name = 'report.invest.repertoire_investissements'

    def get_report_values(self, docids, data=None):
        wizard_record = self.env['reporting.investissement'].browse(data['form'])
        catego_id = data['form']['category_id']
        struct_id = data['form']['structure_id']

        if data['form']['category_id'] and data['form']['structure_id']:
            records = self.env['account.asset.asset'].search(
                [('structure_id', '=', struct_id[0]), ('category_id', '=', catego_id[0]),
                 ('date_aquisition', '<=', data['form']['date_au']), ('faible_valeur', '=', False),
                 ('state', '=', 'open')])
        elif data['form']['structure_id']:
            records = self.env['account.asset.asset'].search(
                [('structure_id', '=', struct_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('state', '=', 'open')])
        elif data['form']['category_id']:
            records = self.env['account.asset.asset'].search(
                [('category_id', '=', catego_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('state', '=', 'open')])
        else:
            records = self.env['account.asset.asset'].search(
                [('date_aquisition', '<=', data['form']['date_au']), ('faible_valeur', '=', False),
                 ('state', '=', 'open')])

        for rec in records:
            if rec.date_sorti:
                if rec.date_sorti <= data['form']['date_au']:
                    records -= rec

        return {
            'doc_model': 'account.asset.asset',
            'docs': records,
            'company_name': records[0].company_id.name if records else 'Cetic',
            'date_au': data['form']['date_au'],
            'company_id': records[0].company_id.id if records else '1'
        }


class invistissementGetValuesRepertoireAssetFaibleValeur(models.AbstractModel):
    _name = 'report.invest.repertoire_invest_faible_valeur'

    def get_report_values(self, docids, data=None):
        struct_id = data['form']['structure_id']

        if data['form']['structure_id']:
            records = self.env['account.asset.asset'].search(
                [('structure_id', '=', struct_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', True), ('state', '!=', 'draft')])
        else:
            records = self.env['account.asset.asset'].search(
                [('date_aquisition', '<=', data['form']['date_au']), ('faible_valeur', '=', True),
                 ('state', '!=', 'draft')])

        return {
            'doc_model': 'account.asset.asset',
            'docs': records,
            'company_name': records[0].company_id.name if records else 'Cetic',
            'date_au': data['form']['date_au'],
            'company_id': records[0].company_id.id if records else '1'
        }


class invistissemenGetValuesDetailAsset(models.AbstractModel):
    _name = 'report.invest.tableau_des_amortissements_detaille'

    def get_report_values(self, docids, data=None):
        wizard_record = self.env['reporting.investissement'].browse(data['form'])
        catego_id = data['form']['category_id']
        struct_id = data['form']['structure_id']

        if data['form']['category_id'] and data['form']['structure_id']:
            records = self.env['account.asset.asset'].search(
                [('structure_id', '=', struct_id[0]), ('category_id', '=', catego_id[0]),
                 ('date_aquisition', '<=', data['form']['date_au']), ('faible_valeur', '=', False),
                 ('state', '=', 'open')])
        elif data['form']['structure_id']:
            affectation = self.env['invest.affectation'].search(
                [('date_affectation', '>=', data['form']['date_du']),
                 ('fin_affectation', '<=', data['form']['date_au']),('structure_id', '=', struct_id[0])])


            records = self.env['account.asset.asset'].search(
                [('structure_id', '=', struct_id[0]),('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('state', '=', 'open')])

            # query = '''SELECT ass.id FROM account.asset.asset as ass, invistissement.affectation as af WHERE af.date_affectation >= ''' + data['form']['date_du'] + '''
            # and af.fin_affectation <=''' + data['form']['date_au'] + ''' and ass.structure_id =''' + struct_id[0] + '''
            # and ass.date_aquisition <=''' + data['form']['date_au'] + '''
            # and faible_valeur = False and ass.state != draft
            # and ass.id = af.asset_id'''
            #
            # self.env.cr.execute(query)
            #
            # # Get the results
            # result = self.env.cr.fetchall()
            # record_ids = [row[0] for row in result]
            #
            # # Use the retrieved record IDs in a domain search
            # records = self.search([('id', 'in', record_ids)])

            # print(affectation)
            # for rec in affectation:
            #     for rec1 in records:
            #         print(rec.asset_id.id)
            #         print(rec1.id)
            #         if rec.asset_id.id == rec1.id:
            #             print('rrr')
            #         else:
            #             records -= rec1

        elif data['form']['category_id']:
            records = self.env['account.asset.asset'].search(
                [('category_id', '=', catego_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('state', '!=', 'draft')])
        else:
            records = self.env['account.asset.asset'].search(
                [('date_aquisition', '<=', data['form']['date_au']), ('faible_valeur', '=', False),
                 ('state', '=', 'open')])


        # records_grouped = get_report_values2(records)
        for rec in records:
            if rec.date_sorti:
                if rec.date_sorti <= data['form']['date_au'] and rec.date_sorti <= data['form']['date_du']:
                    records -= rec
        ordered_test = records.sorted(key=lambda x: x['code'])

        orders_test_grouped = groupby(ordered_test, key=lambda x: x['code'])

        list_grouped = [[order for order in group] for key, group in orders_test_grouped]



        return {
            'doc_model': 'account.asset.asset',
            'docs': list_grouped,
            'company_name': records[0].company_id.name if records else 'Cetic',
            'date_au': data['form']['date_au'],
            'date_du': data['form']['date_du'],
            'company_id': records[0].company_id.id if records else '1'
        }


class invistissementGetValuesRepertoireAssetEtatSortie(models.AbstractModel):
    _name = 'report.invest.repertoire_invest_etat'

    def get_report_values(self, docids, data=None):
        wizard_record = self.env['reporting.investissement'].browse(data['form'])
        catego_id = data['form']['category_id']
        etat_asset_id = data['form']['etat_asset_id']

        if data['form']['etat_asset_id'] and data['form']['category_id']:
            records = self.env['account.asset.asset'].search(
                [('etat_asset_id', '=', etat_asset_id[0]), ('category_id', '=', catego_id[0]),
                 ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '>=', data['form']['date_du']),
                 ('date_sorti', '<=', data['form']['date_au'])])
        elif data['form']['category_id']:
            records = self.env['account.asset.asset'].search(
                [('category_id', '=', catego_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '<=', data['form']['date_au'])])
        elif data['form']['etat_asset_id']:
            records = self.env['account.asset.asset'].search(
                [('etat_asset_id', '=', etat_asset_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '>=', data['form']['date_du']),
                 ('date_sorti', '<=', data['form']['date_au'])])

        else:
            records = self.env['account.asset.asset'].search(
                [('date_aquisition', '<=', data['form']['date_au']), ('date_sorti', '>=', data['form']['date_du']),
                 ('faible_valeur', '=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '<=', data['form']['date_au'])])

        return {
            'doc_model': 'account.asset.asset',
            'docs': records,
            'company_name': records[0].company_id.name if records else 'Cetic',
            'date_au': data['form']['date_au'],
            'date_du': data['form']['date_du'],
            'company_id': records[0].company_id.id if records else '1'
        }


class invistissementGetValuesRepertoireAssetEtatSortieFB(models.AbstractModel):
    _name = 'report.invest.repertoire_invest_etat_fb'

    def get_report_values(self, docids, data=None):
        wizard_record = self.env['reporting.investissement'].browse(data['form'])
        etat_asset_id = data['form']['etat_asset_id']

        if data['form']['etat_asset_id']:
            records = self.env['account.asset.asset'].search(
                [('etat_asset_id', '=', etat_asset_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                 ('faible_valeur', '!=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '>=', data['form']['date_du']),
                 ('date_sorti', '<=', data['form']['date_au'])])
        else:
            records = self.env['account.asset.asset'].search(
                [('date_aquisition', '<=', data['form']['date_au']), ('date_sorti', '>=', data['form']['date_du']),
                 ('faible_valeur', '!=', False), ('etat_asset_id', '!=', False),
                 ('date_sorti', '<=', data['form']['date_au'])])

        return {
            'doc_model': 'account.asset.asset',
            'docs': records,
            'company_name': records[0].company_id.name if records else 'Cetic',
            'date_au': data['form']['date_au'],
            'date_du': data['form']['date_du'],
            'company_id': records[0].company_id.id if records else '1'
        }

    class invistissementGetValuesRepertoireAssetPReforme(models.AbstractModel):
        _name = 'report.invest.repertoire_invest_reforme'

        def get_report_values(self, docids, data=None):
            wizard_record = self.env['reporting.investissement'].browse(data['form'])
            catego_id = data['form']['category_id']
            etat_asset_id = data['form']['etat_asset_id']

            if data['form']['etat_asset_id'] and data['form']['category_id']:
                records = self.env['account.asset.asset'].search(
                    [('etat_asset_id', '=', etat_asset_id[0]), ('category_id', '=', catego_id[0]),
                     ('date_aquisition', '<=', data['form']['date_au']),
                     ('faible_valeur', '=', False), ('state', '=', 'reforme'),
                     ('date_propser', '>=', data['form']['date_du']),
                     ('date_propser', '<=', data['form']['date_au'])])
            elif data['form']['category_id']:
                records = self.env['account.asset.asset'].search(
                    [('category_id', '=', catego_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                     ('faible_valeur', '=', False), ('state', '=', 'reforme'),
                     ('date_propser', '<=', data['form']['date_au'])])
            elif data['form']['etat_asset_id']:
                records = self.env['account.asset.asset'].search(
                    [('etat_asset_id', '=', etat_asset_id[0]), ('date_aquisition', '<=', data['form']['date_au']),
                     ('faible_valeur', '=', False), ('state', '=', 'reforme'),
                     ('date_propser', '>=', data['form']['date_du']),
                     ('date_propser', '<=', data['form']['date_au'])])

            else:
                records = self.env['account.asset.asset'].search(
                    [('date_aquisition', '<=', data['form']['date_au']), ('date_propser', '>=', data['form']['date_du']),
                     ('faible_valeur', '=', False),('state', '=', 'reforme'),
                     ('date_propser', '<=', data['form']['date_au'])])

            return {
                'doc_model': 'account.asset.asset',
                'docs': records,
                'company_name': records[0].company_id.name if records else 'Cetic',
                'date_au': data['form']['date_au'],
                'date_du': data['form']['date_du'],
                'company_id': records[0].company_id.id if records else '1'
            }



# def get_report_values2(records):
#     # Prepare the data for the report
#     report_data = []
#
#     # Group the values based on a field
#     grouped_data = {}  # Dictionary to store the grouped data
#
#     # Assume `records` is the list of records fetched from the database
#     for record in records:
#         group_name = record.code
#         if group_name not in grouped_data:
#             grouped_data[group_name] = []
#
#         grouped_data[group_name].append({
#             'code': record.code,
#             'name': record.name,
#             'numero_inventaire': record.numero_inventaire,
#             'date_aquisition': record.date_aquisition,
#             'value': record.value,
#         })
#
#     # Prepare the grouped data in the required format for the template
#     for group_name, values in grouped_data.items():
#         report_data.append({
#             'group_name': group_name,
#             'values': values,
#         })
#     print(report_data)
#     return report_data
