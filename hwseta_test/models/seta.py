from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Learner(models.Model):
    _name = 'hwseta.learners'

    name = fields.Char()
    id_number = fields.Char()
    qualifications = fields.One2many('learner.qualifications', 'learner')

    @api.constrains('id_number')
    def _check_duplicate_id_number(self):
        for learner in self:
            if self.search_count([('id_number', '=', learner.id_number)]) > 1:
                raise ValidationError("Another learner with the same ID number already exists.")


class Qualifications(models.Model):
    _name = 'hwseta.qualifications'

    def _get_total_credits(self):
        return sum(unit.credit for unit in self.units)

    name = fields.Char()
    units = fields.One2many('hwseta.units', 'qualification')
    total_credit = fields.Integer(compute=_get_total_credits)
    minimum_credits = fields.Integer(string='Minimum Credits to Pass')


class Units(models.Model):
    _name = 'hwseta.units'

    name = fields.Char()
    credit = fields.Integer()
    qualification = fields.Many2one('hwseta.qualifications')


class LearnerQualifications(models.Model):
    _name = 'learner.qualifications'

    qualification = fields.Many2one('hwseta.qualifications')
    learner = fields.Many2one('hwseta.learners')
    credits_achieved = fields.Integer(string='Credits Achieved', compute='_compute_credits_achieved')
    status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Status', compute='_compute_status')

    @api.depends('qualification', 'learner')
    def _compute_credits_achieved(self):
        for rec in self:
            # Compute credits achieved by learner for this qualification
            rec.credits_achieved = sum(unit.credit for unit in rec.qualification.units if unit in rec.learner.units)

    @api.depends('credits_achieved', 'qualification')
    def _compute_status(self):
        for rec in self:
            # Compare credits achieved to minimum credits required
            if rec.credits_achieved >= rec.qualification.minimum_credits:
                rec.status = 'pass'
            else:
                rec.status = 'fail'


class LearnerUnits(models.Model):
    _name = 'learner.units'

    master_unit = fields.Many2one('hwseta.units')
    achieved = fields.Boolean()

class Learner(models.Model):
    _name = 'learner'

    @api.model
    def create_learners(self):
        learner_data = [
            {'name': 'Dylan', 'id_number': '111'},
            {'name': 'Dean', 'id_number': '222'},
            {'name': 'Carol', 'id_number': '333'}
        ]

        for data in learner_data:
            learner = self.create(data)


class QualificationMaster(models.Model):
    _name = 'qualification.master'

    @api.model
    def create_qualifications(self):
        qualifications_data = [
            {'name': 'Computer Science', 'minimum_credits': 20},
            {'name': 'Accounting', 'minimum_credits': 15},
            {'name': 'Agriculture', 'minimum_credits': 12},
            {'name': 'Vetinery Nursing', 'minimum_credits': 12},
            {'name': 'Data Science', 'minimum_credits': 30}
        ]

        for data in qualifications_data:
            qualification = self.create(data)
