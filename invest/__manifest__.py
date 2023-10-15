{
    'name': "invest",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_asset', 'mail', 'purchase', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/report_investissements.xml',
        'data/sequence_invest.xml',
        'data/sequence_dictionnaire.xml',
        'data/type_lieu_data.xml',
        'data/sequence_maintenance.xml',
        'data/sequence_provenance_bien.xml',
        'data/sequence_proposition.xml',
        'data/sequence_attente.xml',
        'data/sequence_reintegration.xml',
        'views/account_views.xml',
        'views/categorie_views.xml',
        'views/endroit_views.xml',
        'views/maintenance_ligne_views.xml',
        'views/type_operation_views.xml',
        'views/type_lieu_views.xml',
        'views/res_config_settings_views.xml',
        'views/etat_asset.xml',
        'views/dictonnaire.xml',
        'views/proposer_reforme.xml',
        'views/type_operation_views.xml',
        'views/provenance_bien.xml',
        'views/motif_proposition.xml',
        # 'views/mise_attente.xml',
        'views/sortie_views.xml',
        'views/reintegration_views.xml',
        'views/sous_compte.xml',
        'views/reporting_views.xml',
        # 'views/immobilisation_test.xml',
        # 'views/product_category_inherit.xml',
        'wizards/reporting_investissement_wizard.xml',
        'wizards/affectation_asset_wizard_views.xml',
        # 'wizards/reporting_views_wizard.xml',
        'wizards/duplication_asset_wizard_views.xml',
        'wizards/ammortissement_ligne_wizard_views.xml',
        'wizards/import_stock_wizard_views.xml',
        'wizards/sortie_invest_wizard.xml',
        'wizards/proposer_reforme_wizard.xml',
        'wizards/reintegration.xml',
        'report/lieu_report.xml',
        'report/repertoire_des_investissements_report.xml',
        'report/asset_code_barre_report.xml',
        'report/decharge_report.xml',
        'report/plan_amortissement_report.xml',
        'report/tableau_des_amortissements_detaille_report.xml',
        'report/repertoire_invest_faible_valeur_report.xml',
        'report/repertoire_invest_par_etat_report.xml',
        'report/repertoire_invest_etat_faibl_report.xml',
        'report/repertoire_invest_proposer_reforme.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
